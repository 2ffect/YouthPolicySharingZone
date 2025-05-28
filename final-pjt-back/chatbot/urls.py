from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot),
    path('profile/', views.save_profile),
]
