"""webproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from app import views

urlpatterns = [
    #path('', views.index),
    path('', views.movies_feed),
    path('news', views.movies_news_feed),
    path('admin/', admin.site.urls),
    path('apply_filters', views.apply_filters),
    path('actors', views.actors_list),
    path('directors', views.directors_list),
    path('movie/<str:movie>/', views.show_movie, name="show_movie"),
    path('actor/<str:actor>/', views.actor_profile, name="actor_profile"),
    path('director/<str:director>/', views.director_profile, name="director_profile"),
    path('newMovies', views.new_movie),
    path('apply_search', views.apply_search),
    path('delete_movie/<str:movie>', views.delete_movie),
    path('apply_searchActor', views.apply_searchActor),
    path('apply_searchDirector', views.apply_searchDirector)
]
