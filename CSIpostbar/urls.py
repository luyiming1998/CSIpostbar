"""CSIpostbar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loginView.as_view()),
    path('login/', views.loginView.as_view()),
    path('logout/', views.logout),
    path('reg/', views.reg),
    path('posts/', views.postsView.as_view()),
    path('index/', views.indexView.as_view()),
    path('myPost/', views.myPostView.as_view()),
    path('myComment/', views.myCommentView.as_view()),
    path('comment/', views.commentView.as_view()),
    path('audioSet/', views.audioSetView.as_view()),
    path('perSet/', views.perSetView.as_view()),
    path('uploadHead/', views.uploadHeadView.as_view()),
    path('userManage/', views.userManageView.as_view()),
    path('editpassword/', views.editpasswordView.as_view()),
    # path('test/',views.test)
]
