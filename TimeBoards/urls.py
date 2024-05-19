from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('track/<int:track_id>/', views.track_leaderboard, name='track_leaderboard'),
    path('car/<int:car_id>/', views.car_leaderboard, name='car_leaderboard'),
    path('games/', views.games, name='games'),
    path('games/<int:game_id>/tracks/', views.tracks, name='tracks'),
    path('games/<int:game_id>/tracks/<int:track_id>/car/<int:car_id>/times/', views.track_times, name='track_times'),
    path('people/<int:person_id>/', views.person_times, name='person_times'),
    path('people/', views.people, name='people'),
    path('add_leaderboard_entry/', views.add_leaderboard_entry, name='add_leaderboard_entry'),
    path('add_event/', views.add_event, name='add_event'),
    path('add_rating/', views.add_rating, name='add_rating'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('games/<int:game_id>/add_car/', views.add_car, name='add_car'),
]