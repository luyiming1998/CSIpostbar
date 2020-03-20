import base64
import json
import os
import re
import uuid

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, HttpResponse, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from CSIpostbar.settings import BASE_DIR
from app01.models import *
from .forms import *
from tools.AipSpeech import client


def check_login(func):
    def wrapper(request, *args, **kwargs):
        user = request.session.get("username")
        print(user)
        if not user:
            return redirect("/login/")
        return func(request, *args, **kwargs)

    return wrapper


def check_admin(func):
    def wrapper(request, *args, **kwargs):
        role = request.session.get("role")
        print(role)
        if role != 1:
            return HttpResponse("普通用户无此权限")
        return func(request, *args, **kwargs)

    return wrapper


# Create your views here.
class loginView(APIView):
    def get(self, request, *args, **kwargs):

        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(userName=username, password=password).values("id", "userName",
                                                                                "password", "role").first()
        if user:
            request.session['user_id'] = user['id']
            request.session['username'] = username
            request.session["role"] = user["role"]
            request.session.set_expiry(360)
            return redirect("/index/")
        else:
            return redirect('/login/')


class indexView(APIView):
    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print(request.session.get("user_id"))
        return render(request, "menu.html")


def reg(request):
    if request.method == "POST":
        regform = RegForm(data=request.POST)
        print(request.POST.get('regEmail'))
        if regform.is_valid():
            regusername = regform.cleaned_data.get("regusername")
            regpassword = regform.cleaned_data.get("regpassword")
            regsex = regform.cleaned_data.get("regsex")
            regAge = regform.cleaned_data.get("regAge")
            regEmial = regform.cleaned_data.get("regEmail")

            User.objects.create(userName=regusername, password=regpassword, regSex=regsex, regAge=regAge,
                                regEmail=regEmial, role=0)
            print(regusername, regAge, regEmial, regpassword, regsex)
            return redirect("/login/")
        else:
            print(regform.errors)


class myPostView(APIView):
    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user_id = request.session.get("user_id")
        postTitle = request.GET.get("postTitle")
        if postTitle:
            articles = Article.objects.filter(postTitle__contains=postTitle, user__id=user_id, status=1).values("id",
                                                                                                                "postTitle",
                                                                                                                "postPageviews",
                                                                                                                "postTime",
                                                                                                                "status",
                                                                                                                "user__userName")
        else:
            articles = Article.objects.filter(user__id=user_id, status=1).values("id", "postTitle", "postPageviews",
                                                                                 "postTime", "status", "user__userName")
        for article in articles:
            print(article)
            comment = Comment.objects.filter(cm_article=article["id"]).order_by("cmTime")
            if comment:
                article["cmPeople"] = comment.count()
                article["cmNewTime"] = comment.first().cmTime
            else:
                article["cmPeople"] = 0
        current_page = request.GET.get('page')
        paginator = Paginator(articles, 10)
        try:
            post = paginator.page(current_page)
        except PageNotAnInteger or EmptyPage as e:
            print(e)
            post = paginator.page(1)
        return render(request, "myPost.html", {"post": post, "searchName": postTitle})

    def post(self, request, *args, **kwargs):
        ret = {'status': True, 'message': None}
        id = request.session.get("user_id")
        title = request.POST.get("title")
        text = request.POST.get("text")
        voice = Voice.objects.filter(user__id=id).values().first()
        print(voice)
        data = re.sub('<.*?>', "", text)
        data = re.sub(r'\n', "", data)
        result = client.synthesis(data, 'zh', 1,
                                  {"spd": voice['auSetSpd'], "pit": voice["auSetPit"], "vol": voice["auSetVol"],
                                   "per": voice["auSetVoiper"]})
        if not isinstance(result, bytes):
            ret = {'status': False, 'message': result.get("err_msg")}
            return HttpResponse(json.dumps(ret))

        # 识别正确返回语音二进制 错误则返回dict
        try:
            re_path = os.path.join('static', 'media', 'postvoice', str(uuid.uuid4()) + '.mp3')
            path = os.path.join(BASE_DIR, re_path)
            if not isinstance(result, dict):
                with open(path, 'wb') as f:
                    f.write(result)
            Article.objects.create(postTitle=title, postText=text, postAudio=os.sep + re_path, user_id=id)
        except Exception as e:
            print(e)
            ret = {'status': False, 'message': e}
        return HttpResponse(json.dumps(ret))

    def delete(self, request, *args, **kwargs):
        ret = {'status': True, 'message': None}
        chk_values = request.POST.getlist("chk_values[]")
        for val in chk_values:
            article = Article.objects.filter(id=val).first()
            if not article:
                ret['status'] = False
                ret['message'] = "该文章不存在"
                return HttpResponse(json.dumps(ret))
            article.status = 0
            article.save()
        return HttpResponse(json.dumps(ret))

class postsView(myPostView):
    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        postTitle = request.GET.get("postTitle")
        if postTitle:
            articles = Article.objects.filter(postTitle__contains=postTitle, status=1).values("id",
                                                                                              "postTitle",
                                                                                              "postPageviews",
                                                                                              "postTime",
                                                                                              "status",
                                                                                              "user__userName")
        else:
            articles = Article.objects.filter(status=1).values("id", "postTitle", "postPageviews",
                                                               "postTime", "status", "user__userName")
        for article in articles:
            print(article)
            comment = Comment.objects.filter(cm_article=article["id"]).order_by("cmTime")
            if comment:
                article["cmPeople"] = comment.count()
                article["cmNewTime"] = comment.first().cmTime
            else:
                article["cmPeople"] = 0
        current_page = request.GET.get('page')
        paginator = Paginator(articles, 10)
        try:
            post = paginator.page(current_page)
        except PageNotAnInteger or EmptyPage as e:
            print(e)
            post = paginator.page(1)
        return render(request, "post.html", {"post": post, "searchName": postTitle})



class myCommentView(APIView):
    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.GET.get("ajax"):
            ret = {'status': True, 'message': None}
            cm_id = request.GET.get("cm_id")
            comment = Comment.objects.filter(id=cm_id).first()
            if comment:
                ret['text'] = comment.cmText
            else:
                ret = {'status': False, 'message': "无此评论"}
            return HttpResponse(json.dumps(ret))
        user_id = request.session.get("user_id")
        print(user_id)
        comments = Comment.objects.filter(cm_user_id=user_id, status=1).values("id",
                                                                               "cmText",
                                                                               "cmAudio",
                                                                               "cmTime",
                                                                               "cm_article__postTitle",
                                                                               "cm_article__id",
                                                                               "cm_user__userName",
                                                                               "cmAudio",
                                                                               "support")
        current_page = request.GET.get('page')
        paginator = Paginator(comments, 10)
        try:
            post = paginator.page(current_page)
        except PageNotAnInteger or EmptyPage as e:
            print(e)
            post = paginator.page(1)
        print(comments)
        return render(request, "myComment.html", {"post": post})

    def delete(self, request, *args, **kwargs):
        ret = {'status': True, 'message': None}
        chk_values = request.POST.getlist("chk_values[]")
        for val in chk_values:
            comment = Comment.objects.filter(id=val).first()
            if not comment:
                ret['status'] = False
                ret['message'] = "id为" + val + "的评论不存在"
                return HttpResponse(json.dumps(ret))
            comment.status = 0
            comment.save()
        return HttpResponse(json.dumps(ret))

    def put(self, request, *args, **kwargs):
        ret = {'status': True, 'message': None}
        id = request.session.get("user_id")
        cm_id = request.POST.get("cm_id")
        cmText = request.POST.get("cmText")
        voice = Voice.objects.filter(user__id=id).values().first()
        data = re.sub('<.*?>', "", cmText)
        data = re.sub(r'\n', "", data)
        result = client.synthesis(data, 'zh', 1,
                                  {"spd": voice['auSetSpd'], "pit": voice["auSetPit"], "vol": voice["auSetVol"],
                                   "per": voice["auSetVoiper"]})
        if not isinstance(result, bytes):
            ret = {'status': False, 'message': result.get("err_msg")}
            return HttpResponse(json.dumps(ret))

        # 识别正确返回语音二进制 错误则返回dict
        try:
            re_path = os.path.join('static', 'media', 'postvoice', str(uuid.uuid4()) + '.mp3')
            path = os.path.join(BASE_DIR, re_path)
            if not isinstance(result, dict):
                with open(path, 'wb') as f:
                    f.write(result)
            Comment.objects.filter(id=cm_id).update(cmText=cmText, cmAudio=os.sep + re_path)
        except Exception as e:
            print(e)
            ret = {'status': False, 'message': e}
        return HttpResponse(json.dumps(ret))


class audioSetView(APIView):
    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        id = request.session.get("user_id")
        voice = Voice.objects.filter(user__id=id).first()
        return render(request, "audioSet.html", {"voice": voice})

    def post(self, request, *args, **kwargs):

        ret = {'status': True, 'message': None}
        id = request.session.get("user_id")
        auSetVoiPer = request.POST.get("auSetVoiPer")
        auSetSpd = request.POST.get("auSetSpd")
        auSetPit = request.POST.get("auSetPit")
        auSetVol = request.POST.get("auSetVol")
        try:
            voice = Voice.objects.filter(auSetVoiper=auSetVoiPer, auSetSpd=auSetSpd, auSetPit=auSetPit,
                                         auSetVol=auSetVol).first()
            User.objects.filter(id=id).update(voice=voice)
        except Exception as e:
            print(e)
            ret = {'status': False, 'message': "修改失败"}
        return HttpResponse(json.dumps(ret))


class perSetView(APIView):
    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user_id = request.session.get("user_id")
        user = User.objects.filter(id=user_id).first()
        return render(request, "perSet.html", {"user": user})

    def put(self, request, *args, **kwargs):
        ret = {'status': True, 'message': None}

        id = request.POST.get("id")
        userName = request.POST.get("userName")
        oldName = request.POST.get("oldName")
        user = User.objects.filter(id=id, userName=oldName).first()
        if not user:
            ret["status"] = False
            ret["message"] = "无此用户"
            return HttpResponse(json.dumps(ret))
        if not userName == oldName:
            check_Name = User.objects.filter(userName=userName)
            if check_Name:
                ret["status"] = False
                ret["message"] = "新用户名重名"
                return HttpResponse(json.dumps(ret))
            user.userName = userName
        regsex = request.POST.get("regsex")
        regAge = request.POST.get("regAge")
        regEmail = request.POST.get("regEmail")
        user.regSex = regsex
        user.regAge = regAge
        user.regEmail = regEmail
        user.save()
        return HttpResponse(json.dumps(ret))


class uploadHeadView(APIView):
    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user_id = request.session.get("user_id")
        user = User.objects.filter(id=user_id).first()
        return render(request, "uploadHead.html", {"regPhoto": user.regPhoto})

    def post(self, request, *args, **kwargs):
        ret = {'status': True, 'message': None}
        data = request.POST.get('file')
        file = base64.b64decode(data)
        id = request.session.get("user_id")
        re_path = os.path.join('static', 'media', 'headphoto', str(uuid.uuid4()) + '.jpg')
        path = os.path.join(BASE_DIR, re_path)
        try:
            with open(path, 'wb') as f:
                f.write(file)
            print(path)
            User.objects.filter(id=id).update(regPhoto=os.sep + re_path)
        except Exception as e:
            print(e)
            ret = {'status': False, 'message': "上传失败"}
        finally:
            return HttpResponse(json.dumps(ret))


class userManageView(APIView):
    @method_decorator(check_login)
    @method_decorator(check_admin)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        userName = request.GET.get("userName")
        if userName:
            users = User.objects.filter(userName__contains=userName, status=1)
        else:
            users = User.objects.filter(status=1)
        current_page = request.GET.get('page')
        paginator = Paginator(users, 10)
        try:
            post = paginator.page(current_page)
        except PageNotAnInteger or EmptyPage as e:
            post = paginator.page(1)

        return render(request, "userManage.html", {"post": post, "searchName": userName})

    def put(self, request, *args, **kwargs):
        ret = {'status': True, 'message': None}

        id = request.POST.get("id")
        userName = request.POST.get("userName")
        oldName = request.POST.get("oldName")
        user = User.objects.filter(id=id, userName=oldName).first()
        if not user:
            ret["status"] = False
            ret["message"] = "无此用户"
            return HttpResponse(json.dumps(ret))
        if not userName == oldName:
            check_Name = User.objects.filter(userName=userName)
            if check_Name:
                ret["status"] = False
                ret["message"] = "新用户名重名"
                return HttpResponse(json.dumps(ret))
            user.userName = userName
        regsex = request.POST.get("regsex")
        regAge = request.POST.get("regAge")
        regEmail = request.POST.get("regEmail")
        role = request.POST.get("role")
        password = request.POST.get("password")
        user.regSex = regsex
        user.regAge = regAge
        user.regEmail = regEmail
        user.role = role
        if not password:
            user.password = password
        user.save()

        return HttpResponse(json.dumps(ret))

    def delete(self, request, *args, **kwargs):
        ret = {'status': True, 'message': None}
        chk_values = request.POST.getlist("chk_values[]")
        for val in chk_values:
            user = User.objects.filter(id=val).first()
            if not user:
                ret['status'] = False
                ret['message'] = "id为" + val + "的用户不存在"
                return HttpResponse(json.dumps(ret))
            user.status = 0
            user.save()
        return HttpResponse(json.dumps(ret))


class editpasswordView(APIView):
    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        return render(request, "editpassword.html")

    def post(self, request, *args, **kwargs):
        ret = {'status': True, 'message': None}
        id = request.session.get("user_id")
        newPassword = request.POST.get("newPassword")
        oldPassword = request.POST.get("oldPassword")
        user = User.objects.filter(id=id)
        if oldPassword != user.first().password:
            ret = {'status': False, 'message': "原密码不正确，请重新输入"}
            return HttpResponse(json.dumps(ret))
        elif newPassword == oldPassword:
            ret = {'status': False, 'message': "新密码与原密码不能相同"}
            return HttpResponse(json.dumps(ret))
        else:
            User.objects.filter(id=id).update(password=newPassword)
            return HttpResponse(json.dumps(ret))


def logout(request):
    request.session.flush()
    return redirect('/login/')


# def test(request):
#     for per in range(0, 2):
#         for vol in range(0, 16):
#             for pit in range(0, 10):
#                 for spd in range(0, 10):
#                     Voice.objects.create(auSetVol=vol, auSetVoiper=per, auSetSpd=spd, auSetPit=pit)
#     for per in range(3, 5):
#         for vol in range(0, 16):
#             for pit in range(0, 10):
#                 for spd in range(0, 10):
#                     Voice.objects.create(auSetVol=vol, auSetVoiper=per, auSetSpd=spd, auSetPit=pit)
#     return HttpResponse(1111)
class commentView(APIView):
    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        page=request.GET.get("page")
        post_id = request.GET.get("post_id")
        article = Article.objects.filter(id=post_id).values("id", "postTitle", "postText", "postTime", "postAudio",
                                                            "user__userName", "user__regTime", "user__regPhoto").first()
        print(article)
        comments = Comment.objects.filter(cm_article_id=article["id"], status=1).order_by("cmTime").values("id",
                                                                                                           "cmText",
                                                                                                           "cmAudio",
                                                                                                           "cmTime",
                                                                                                           "cm_user__userName",
                                                                                                           "cm_user__regTime",
                                                                                                           "cmAudio",
                                                                                                           "cm_user__regPhoto",
                                                                                                           "support")
        print(comments)
        return render(request, 'comment.html', {"article": article, "comments": comments,"page":page})

    def post(self, request, *args, **kwargs):
        ret = {'status': True, 'message': None}
        id = request.session.get("user_id")
        cmText = request.POST.get("cmText")
        article_id = request.POST.get("article_id")
        voice = Voice.objects.filter(user__id=id).values().first()
        print(voice)
        data = re.sub('<.*?>', "", cmText)
        data = re.sub(r'\n', "", data)
        result = client.synthesis(data, 'zh', 1,
                                  {"spd": voice['auSetSpd'], "pit": voice["auSetPit"], "vol": voice["auSetVol"],
                                   "per": voice["auSetVoiper"]})
        if not isinstance(result, bytes):
            ret = {'status': False, 'message': result.get("err_msg")}
            return HttpResponse(json.dumps(ret))

        # 识别正确返回语音二进制 错误则返回dict
        try:
            re_path = os.path.join('static', 'media', 'postvoice', str(uuid.uuid4()) + '.mp3')
            path = os.path.join(BASE_DIR, re_path)
            if not isinstance(result, dict):
                with open(path, 'wb') as f:
                    f.write(result)
            Comment.objects.create(cmText=cmText, cmAudio=os.sep + re_path, cm_user_id=id, cm_article_id=article_id)
        except Exception as e:
            print(e)
            ret = {'status': False, 'message': e}
        return HttpResponse(json.dumps(ret))

    def delete(self, request, *args, **kwargs):
        ret = {'status': True, 'message': None}
        chk_values = request.POST.getlist("chk_values[]")
        for val in chk_values:
            comment = Comment.objects.filter(id=val).first()
            if not comment:
                ret['status'] = False
                ret['message'] = "id为" + val + "的评论不存在"
                return HttpResponse(json.dumps(ret))
            comment.status = 0
            comment.save()
        return HttpResponse(json.dumps(ret))
