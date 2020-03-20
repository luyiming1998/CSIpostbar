from django.db import models


# Create your models here.
class User(models.Model):
    userName = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=32)
    regAge = models.IntegerField()
    regSex = models.IntegerField()
    regEmail = models.EmailField(max_length=255)
    regPhoto = models.ImageField(upload_to='headphoto',default="/static/headPhoto/default/default.jpg")
    regTime = models.DateTimeField(auto_now=True)
    loginTime = models.DateTimeField(auto_now=True)
    role_choices=(
        (0,"普通用户"),
        (1,"管理员")
    )
    role = models.IntegerField(choices=role_choices)
    status = models.IntegerField(default=1)
    voice = models.ForeignKey("Voice", on_delete=models.CASCADE, default=2085)


class Voice(models.Model):
    auSetVol = models.IntegerField()
    auSetVoiper = models.IntegerField()
    auSetSpd = models.IntegerField()
    auSetPit = models.IntegerField()


class Article(models.Model):
    postTitle = models.CharField(max_length=16)
    postText = models.TextField()
    postPageviews = models.IntegerField(default=0)
    postAudio = models.CharField(max_length=255)
    postTime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)


class Comment(models.Model):
    cmText = models.TextField()
    cmAudio = models.CharField(max_length=255)
    cmTime = models.DateTimeField(auto_now=True)
    cm_article = models.ForeignKey(Article, on_delete=models.CASCADE)
    cm_user = models.ForeignKey(User, on_delete=models.CASCADE)
    support = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
