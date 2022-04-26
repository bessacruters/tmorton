from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('add', views.add),
    path('add-page', views.addPage),
    path('pages/delete/<idd>', views.deletePage),
    path('pages/edit/<idd>', views.editPage),

    path('categories', views.categories),
    path('categories/add', views.addCategory),
    path('categories/edit/<idd>', views.editCategory),
    path('categories/delete/<idd>', views.deleteCategory),

    path('users', views.users),
    path('users/delete/<idd>', views.deleteUser),

    path('logout', views.handle_logout),

    path('about', views.aboutView),
    path('about/save', views.saveAbout),
]