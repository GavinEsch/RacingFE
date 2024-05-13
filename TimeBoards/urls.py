from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('track/<int:track_id>/', views.track_leaderboard, name='track_leaderboard'),
    path('car/<int:car_id>/', views.car_leaderboard, name='car_leaderboard'),
    path('add-entry/', views.create_leaderboard_entry, name='create_leaderboard_entry'),
]
