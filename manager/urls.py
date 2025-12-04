from django.urls import path

from . import views

urlpatterns = [
    path('voices', views.list_all_voices),
]
