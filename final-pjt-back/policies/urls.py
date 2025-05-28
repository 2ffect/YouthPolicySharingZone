from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
  path('<str:keyword>/', views.filter_policies),
  path('policy_detail/<int:policy_id>/', views.policy_detail),
  path('policy_detail/<int:policy_id>/scrap/', views.scrap_policy),
  path('policy_detail/<int:policy_id>/is_scrapped/', views.is_policy_scrapped),
]
