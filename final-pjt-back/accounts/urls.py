"""
URL configuration for finproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from .views import CustomLoginView, ScrapedPolicesView, ScrapedArticlesView
from dj_rest_auth.views import LogoutView, PasswordChangeView, UserDetailsView

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('user/', UserDetailsView.as_view(), name='rest_user_details'),
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    path('login/', CustomLoginView.as_view(), name='rest_login'),
    path('signup/', include('dj_rest_auth.registration.urls')),
    path('policy_scrap/', ScrapedPolicesView.as_view() ),
    path('article_scrap/', ScrapedArticlesView.as_view() ),
    

]
