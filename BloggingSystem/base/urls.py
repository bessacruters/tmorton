from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('accounts/login', views.loginpage),
    path('dologin', views.handle_login),
    path('accounts/signup', views.register),
    path('doregister', views.handle_register),
    path('logout', views.handle_logout),

    path('category/<idd>', views.categoryPage),
    path('pages/<idd>', views.viewPage),

    path('accounts/profile/<idd>', views.viewProfile),
    path('accounts/profile/edit/<idd>', views.editProfile),
    path('accounts/delete/<idd>', views.deleteAccount),

    path('search', views.search),
    path('about', views.viewAbout),

    path('messages', views.viewMessages),
    path('messages/send', views.sendMessage),
    path('get-msgs', views.getmessages),
]