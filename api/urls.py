from django.urls import path

from . import views

urlpatterns = [
    path('voices', views.submit_voice),
]
