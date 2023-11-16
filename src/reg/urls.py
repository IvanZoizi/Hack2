from django.contrib import admin
from django.urls import path
from views import Register

urlpatterns = [
    path('company/', Register.as_view(), name='reg-company')
]
