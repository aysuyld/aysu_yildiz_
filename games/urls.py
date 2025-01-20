# games/urls.py

from django.urls import path
#from django.contrib.auth import views as auth_view
from . import views
#from . import api_views
from . import auth_views

urlpatterns = [
    # Web URLs
    path('', views.base_view, name='base'),
    path('home', views.HomeView.as_view(), name='home'),
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('games/', views.GamesHomeView.as_view(), name='games_home'),
    path('maze_coding/', views.MazeCodingView.as_view(), name='maze_coding'),
]