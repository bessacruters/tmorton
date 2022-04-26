import os
from pathlib import Path
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from base.models import UserInfo, about, category, post, message
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.utils import formats



BASE_DIR = Path(__file__).resolve().parent

def home(request):
    categories = list(category.objects.all())
    data = []
    for cat in categories:
        catDict = model_to_dict(cat)
        catDict['posts'] = post.objects.filter(category=cat.id)[:7]
        data.append(catDict)

    data = {'categories': data}
    return render(request, 'home.html', data)


def loginpage(request):
    categories = list(category.objects.all())
    return render(request, 'login.html', {'categories': categories})

def register(request):
    categories = list(category.objects.all())
    return render(request, 'register.html', {'categories': categories})

def handle_login(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user_obj = User.objects.filter(username=loginusername).first()
        if user_obj:
            username = user_obj.username
            user = authenticate(request, username=loginusername, password=loginpass)
            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    messages.success(request, username + ' Sucessfully logged as Admin.')
                    return redirect('/admin')
                else:
                    messages.success(request, username + ' Sucessfully logged in')
                    return redirect('/')
        messages.error(request, 'Invalid User name or password')
    return render(request, 'login.html')


def handle_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if len(username) > 15:
            messages.error(request, 'Username must be under 15 characters')
            return redirect('/accounts/signup')

        elif (pass1 != pass2) or not pass1:
            messages.error(request, 'Passwords do not match')
            return redirect('/accounts/signup')

        elif not username.isalnum():
            messages.error(request, 'Username should only contain letters and numbers')
            return redirect('/accounts/signup')

        elif User.objects.filter(username=username).exists():
            messages.error(request, 'User already exist')
            return redirect('/accounts/signup')

        else:
            myuser = User(first_name=name, username=username , email=email, password = make_password(pass1))
            info = UserInfo(image = '/static/profile-images/place-holder.png', description= '', websiteLink = '', userName = username)
            myuser.save()
            info.save()
            messages.success(request, 'Account created Successfully')
            return redirect('/accounts/login')

    return render(request, 'register.html')

def handle_logout(request):
    logout(request)
    messages.success(request, 'Logged out Successfully')
    return redirect('/accounts/login')

def categoryPage(request, idd):
    categories = list(category.objects.all())
    posts = post.objects.filter(category=idd)
    cat_Name = category.objects.filter(id=idd).first().name
    return render(request, 'category.html', {'categories': categories, 'posts': posts, 'cat_Name': cat_Name})

def viewPage(request, idd):
    viewPost = post.objects.filter(id=idd).first()
    relatedPosts = post.objects.filter(category=viewPost.category.id).exclude(id=viewPost.id)
    categories = list(category.objects.all())
    cat_Name = category.objects.filter(id=viewPost.category.id).first().name
    return render(request, 'page.html', {'categories': categories, 'post': viewPost, 'relatedPosts': relatedPosts , 'cat_Name': cat_Name})

def viewProfile(request, idd):
    if request.user.is_authenticated:
        categories = list(category.objects.all())
        userObj = User.objects.filter(id=idd).first()
        userInfo = UserInfo.objects.filter(userName = userObj.username).first()
        return render(request, 'profile.html', {'categories': categories, 'user': userObj, 'userInfo': userInfo })
    else:
        messages.error(request, 'You are not logged. Please login first.')
        return redirect('/')

def editProfile(request, idd):
    if request.user.is_authenticated:
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if (pass1 != pass2):
            messages.error(request, 'Passwords do not match')
            return redirect('/accounts/profile/' + idd)

        userObj = User.objects.filter(id=idd).first()
        userInfo = UserInfo.objects.filter(userName = userObj.username).first()

        userFullName = request.POST['name']
        userEmail = request.POST['email']
        infodescription = request.POST['description']
        infoWebsite = request.POST['websiteLink']

        if pass1 != "":
            userObj.password = make_password(pass1)

        userObj.first_name = userFullName
        userObj.email = userEmail
        userInfo.description = infodescription
        userInfo.websiteLink = infoWebsite

        if len(request.FILES) != 0:
            upload = request.FILES['image']
            fss = FileSystemStorage()

            MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static\\profile-images\\')
            file = fss.save(MEDIA_ROOT + upload.name, upload)
            file_url = fss.url(file)
            userInfo.image = file_url

        userObj.save()
        userInfo.save()

        messages.success(request, 'Profile Saved Successfully')
        return redirect('/accounts/profile/' + idd)
    else:
        messages.error(request, 'You are not logged. Please login first.')
        return redirect('/')

def deleteAccount(request, idd):
    if request.user.is_authenticated:
        userObj = User.objects.filter(id=idd).first()
        userInfo = UserInfo.objects.filter(userName = userObj.username).first()

        userInfo.delete()
        userObj.delete()
        logout(request)
        messages.success(request, 'Account Deleted Successfully')
        return redirect('/')
    else:
        messages.error(request, 'You are not logged. Please login first.')
        return redirect('/')


def search(request):
    query = request.GET['query']
    categories = list(category.objects.all())
    posts = post.objects.filter(Q(title__contains=query) | Q(content__contains=query))
    return render(request, 'search.html', {'categories': categories, 'posts': posts, 'query': query})

def viewAbout(request):
    categories = list(category.objects.all())
    posts = list(post.objects.all()[:5])

    aboutsAll = about.objects.all()
    if(aboutsAll):
        aboutContent = aboutsAll[0].content
        return render(request, 'about.html',  {'categories': categories, 'aboutContent': aboutContent, 'relatedPosts': posts})
    else:
        return render(request, 'about.html',  {'categories': categories, 'aboutContent': '', 'relatedPosts': posts})

def viewMessages(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You are not logged. Please login first.')
        return redirect('/')
    
    categories = list(category.objects.all())
    messagess = message.objects.all()

    return render(request, 'messages.html',  {'categories': categories, 'messagess': messagess})

def getmessages(request):
    if not request.user.is_authenticated:
        return JsonResponse({"messages":[]})
        
    all_messages= list(message.objects.all().order_by('-created')[:50])
    data = []
    for msg in all_messages:
        msgDict = model_to_dict(msg)
        msgDict['created'] = formats.date_format(msg.created, "SHORT_DATETIME_FORMAT") 
        userObj = User.objects.filter(id=msg.user.id).exclude(is_superuser=True).first()
        userInfo = UserInfo.objects.filter(userName = userObj.username).first()
        msgDict['user'] =  model_to_dict(userObj)
        msgDict['usreInfo'] = model_to_dict(userInfo)

        if msg.user.id == request.user.id:
            msgDict['side'] = 'right'
        else:
            msgDict['side'] = 'left'

        data.append(msgDict)

    return JsonResponse({"messages":list(data)})

def sendMessage(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status":"failed"})

    if request.method == "POST":
        msg = request.POST['msg']
        msg = message(content = msg, user = request.user)
        msg.save()
        return JsonResponse({"status":"success"})
    
    return JsonResponse({"status":"failed"})
