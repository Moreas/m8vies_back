"""french_movies_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from movies import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('genres/', views.get_genres),
    path('movies/', views.get_movies),
    path('favorite_movies/', views.get_fav_movies),
    path('search_movies/', views.search_movies),
    path('movie/<int:id>', views.get_movie),
    path('featured_movie/', views.get_featured_movie),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('fav_movie/<int:id>', views.fav_movie),
    path('unfav_movie/<int:id>', views.unfav_movie),
    path('fav_movies_list/', views.get_fav_movies_list),
    path('check_user_token/', views.check_user_token),
    path('create_auth/', views.create_auth)
]
