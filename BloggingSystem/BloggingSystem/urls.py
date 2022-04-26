from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', include('admin.urls')),
    path('', include('base.urls'))
]
