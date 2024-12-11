
from django.contrib import admin
from django.urls import path,include
from users.views import LOGIN
from . import views

urlpatterns = [
    path('',LOGIN,name='login'),
    path('users/',include('users.urls') ),

]
