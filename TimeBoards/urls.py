from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('track/<int:track_id>/', views.track_leaderboard, name='track_leaderboard'),
    path('car/<int:car_id>/', views.car_leaderboard, name='car_leaderboard'),
    path('games/', views.games, name='games'),
    path('games/<int:game_id>/tracks/', views.tracks, name='tracks'),
    path('games/<int:game_id>/tracks/<int:track_id>/', views.track_leaderboard, name='track_leaderboard'),
    path('games/<int:game_id>/tracks/<int:track_id>/car/<int:car_id>/times/', views.track_times, name='track_times'),
    path('people/<int:person_id>/', views.person_times, name='person_times'),
    path('people/', views.people, name='people'),
    
]
