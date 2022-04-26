from email.mime import image
from importlib.resources import contents
from pathlib import Path
from tempfile import NamedTemporaryFile
import time
from urllib.request import urlopen
from django.shortcuts import redirect, render
from base.models import UserInfo, category, post, about
from django.conf import settings as django_settings
import os
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


BASE_DIR = Path(__file__).resolve().parent


def home(request):
    categories = list(category.objects.all())
    posts = list(post.objects.all())
    return render(request, 'admin/home.html', {'posts': posts})


def add(request):
    categories = list(category.objects.all())
    return render(request, 'admin/add.html', {'categories': categories})

def addPage(request):
    upload = request.FILES['image']
    fss = FileSystemStorage()

    MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static\\posts-images\\')
    file = fss.save(MEDIA_ROOT + upload.name, upload)
    file_url = fss.url(file)


    postTitle = request.POST['title']
    postContent = request.POST['content']
    postCategory = category.objects.filter(id=request.POST['category']).first()
    postImgDate = request.POST['imageDate']

    new_post = post(title= postTitle, content= postContent, category=postCategory, imageDate = postImgDate, image = file_url )
    new_post.save()

    messages.success(request, 'Page Addedd Successfully.')
    return redirect('/admin')

def deletePage(request, idd):
    delete_post = post.objects.filter(id=idd).first()
    delete_post.delete()
    messages.success(request, 'Page Delete Successfully.')
    return redirect('/admin')

def editPage(request, idd):
    editPost = post.objects.filter(id=idd).first()
    if request.method == 'POST':
        postTitle = request.POST['title']
        postContent = request.POST['content']
        postCategory = category.objects.filter(id=request.POST['category']).first()
        postImgDate = request.POST['imageDate']

        editPost.title = postTitle
        editPost.content = postContent
        editPost.category = postCategory
        editPost.imageDate = postImgDate

        if len(request.FILES) != 0:
            upload = request.FILES['image']
            fss = FileSystemStorage()

            MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static\\posts-images\\')
            file = fss.save(MEDIA_ROOT + upload.name, upload)
            file_url = fss.url(file)
            editPost.image = file_url

        editPost.save()
        messages.success(request, 'Page Updated Successfully.')
        return redirect('/admin')
    else:
        categories = list(category.objects.all())
        return render(request, 'admin/edit.html',  {'categories': categories, 'post': editPost})

def categories(request):
    categories = list(category.objects.all())
    return render(request, 'admin/categories.html',  {'categories': categories})

def addCategory(request):
    catname = request.POST['name']
    add_category = category(name= catname)
    add_category.save()
    messages.success(request, 'Category Addedd Successfully.')
    return redirect('/admin/categories')

def editCategory(request, idd):
    editCat = category.objects.filter(id=idd).first()
    catname = request.POST['name']
    editCat.name = catname
    editCat.save()
    messages.success(request, 'Category Updated Successfully.')
    return redirect('/admin/categories')

def deleteCategory(request, idd):
    delete_cat = category.objects.filter(id=idd).first()
    delete_cat.delete()
    messages.success(request, 'Category Delete Successfully.')
    return redirect('/admin/categories')

def users(request):
    users = list(User.objects.all().exclude(is_superuser=True))
    return render(request, 'admin/users.html',  {'users': users})

def deleteUser(request, idd):
    userObj = User.objects.filter(id=idd).first()
    userInfo = UserInfo.objects.filter(userName = userObj.username).first()

    userInfo.delete()
    userObj.delete()
    
    messages.success(request, 'User Delete Successfully.')
    return redirect('/admin/users')

def handle_logout(request):
    logout(request)
    messages.success(request, 'Logged out Successfully')
    return redirect('/accounts/login')

def aboutView(request):
    aboutsAll = about.objects.all()
    if(aboutsAll):
        aboutContent = aboutsAll[0].content
        return render(request, 'admin/about.html',  {'aboutContent': aboutContent})
    else:
        return render(request, 'admin/about.html',  {'aboutContent': ''})

def saveAbout(request):
    abouts = about.objects.all()
    aboutContent = request.POST['content']

    if(abouts):
        oldAbout = abouts[0]
        oldAbout.content = aboutContent
        oldAbout.save()
    else:
        newAbout = about(content = aboutContent)
        newAbout.save()

    messages.success(request, 'About page Updated Successfully')
    return redirect('/admin/about')