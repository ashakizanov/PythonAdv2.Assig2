
from django.contrib import admin
from django.urls import path
from graphs.views import home


urlpatterns = [
    path('', home, name='home'),
]
