from datetime import datetime
from django.conf import settings
from django.db import models

# Create your models here.

class UserInfo(models.Model):
    image = models.CharField(max_length=100)
    description = models.TextField()
    websiteLink = models.CharField(max_length=200)
    userName = models.CharField(max_length=50)

class category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    

class post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    imageDate = models.DateTimeField()
    content = models.TextField()
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

class about(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()

class message(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    created = models.DateTimeField(auto_now_add=True, null=True)