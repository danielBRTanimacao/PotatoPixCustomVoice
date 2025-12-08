from django.urls import path

from . import views

urlpatterns = [
    path('voices', views.ManagerCustomVoice.as_view()),
    path('voices/<int:pk>', views.ManagerCustomVoice.as_view())
]
