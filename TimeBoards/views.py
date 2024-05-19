from django.shortcuts import render, redirect, get_object_or_404
from .models import (LeaderboardEntry, Track, Car, Game, User, Session, Attempt, TelemetryData, Achievement, Comment, Event, Rating, UserAchievement)
from .forms import (LeaderboardEntryForm, GameForm, TrackForm, CarForm, SessionForm, AttemptForm, TelemetryDataForm, AchievementForm, UserAchievementForm, CommentForm, EventForm, RatingForm)
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm 

import json
from datetime import timedelta
from django.conf import settings

def homepage(request):
    entries = LeaderboardEntry.objects.all().select_related('track', 'car', 'game', 'user').order_by('track', 'car', 'time')
    top_times = {}
    for entry in entries:
        key = (entry.track, entry.car, entry.game)
        if key not in top_times:
            top_times[key] = entry
    return render(request, 'TimeBoards/homepage.html', {'entries': top_times.values()})

def games(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('games')
    else:
        form = GameForm()
    games = Game.objects.all()
    return render(request, 'TimeBoards/games.html', {'games': games, 'form': form})

def tracks(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    tracks = Track.objects.filter(game=game)
    tracks_with_cars = []

    for track in tracks:
        car = track.cars.first()  # Assuming one car per track
        if car:
            tracks_with_cars.append((track, car))

    if request.method == 'POST':
        form = TrackForm(request.POST, request.FILES)
        if form.is_valid():
            track = form.save(commit=False)
            track.game = game
            track.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('tracks', game_id=game.id)
        else:
            print(form.errors)  # Debug: Print form errors to console
    else:
        form = TrackForm()
        car_form = CarForm()

    game_settings = json.loads(game.settings) if isinstance(game.settings, str) else game.settings
    game_settings = game_settings.get('gameSettings', {})

    return render(request, 'TimeBoards/tracks.html', {
        'game': game,
        'tracks_with_cars': tracks_with_cars,
        'form': form,
        'car_form': car_form,
        'game_settings': game_settings
    })

def add_car(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.game = game  # Associate the car with the game
            car.save()
            return redirect('tracks', game_id=game_id)
        else:
            print(form.errors)  # Debug: Print form errors to console
    else:
        form = CarForm()
    return render(request, 'TimeBoards/add_car.html', {'form': form})

def people(request):
    all_people = User.objects.all()
    print("All people:", all_people)  # Debug: Print all users to the console
    print("Database config:", settings.DATABASES)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('people')  # Redirect to refresh the page and show the new person
        else:
            print(form.errors)  # Debug: Print form errors to the console
    else:
        form = CustomUserCreationForm()
    return render(request, 'TimeBoards/people.html', {'people': all_people, 'form': form})


def person_times(request, person_id):
    person = get_object_or_404(User, id=person_id)
    times = LeaderboardEntry.objects.filter(user=person).order_by('time')
    return render(request, 'TimeBoards/person_times.html', {'person': person, 'times': times})

def track_times(request, game_id, track_id, car_id):
    game = get_object_or_404(Game, id=game_id)
    track = get_object_or_404(Track, id=track_id, game=game)
    car = get_object_or_404(Car, id=car_id, game=game, tracks=track)
    times = LeaderboardEntry.objects.filter(track=track, car=car, game=game).order_by('time')

    if request.method == 'POST':
        form = LeaderboardEntryForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            minutes = form.cleaned_data['minutes']
            seconds = form.cleaned_data['seconds']
            milliseconds = form.cleaned_data['milliseconds']

            new_time = timedelta(minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))

            try:
                existing_entry = LeaderboardEntry.objects.get(track=track, car=car, user=user, game=game)
                if new_time < existing_entry.time:
                    existing_entry.time = new_time
                    existing_entry.save()
            except LeaderboardEntry.DoesNotExist:
                entry = form.save(commit=False)
                entry.track = track
                entry.car = car
                entry.game = game
                entry.time = new_time
                entry.save()

            return redirect('track_times', game_id=game_id, track_id=track_id, car_id=car_id)
        else:
            print(form.errors)  # Debug: Print form errors to console
    else:
        form = LeaderboardEntryForm()

    return render(request, 'TimeBoards/track_times.html', {'game': game, 'track': track, 'car': car, 'times': times, 'form': form})



def track_leaderboard(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    entries = LeaderboardEntry.objects.filter(track=track).order_by('time')[:10]
    return render(request, 'TimeBoards/track_leaderboard.html', {'track': track, 'entries': entries})

def car_leaderboard(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    entries = LeaderboardEntry.objects.filter(car=car).order_by('time')[:10]
    return render(request, 'TimeBoards/car_leaderboard.html', {'car': car, 'entries': entries})

def add_leaderboard_entry(request):
    if request.method == 'POST':
        form = LeaderboardEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = LeaderboardEntryForm()
    return render(request, 'TimeBoards/add_leaderboard_entry.html', {'form': form})

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = EventForm()
    return render(request, 'TimeBoards/add_event.html', {'form': form})

def add_rating(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = RatingForm()
    return render(request, 'TimeBoards/add_rating.html', {'form': form})

def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = CommentForm()
    return render(request, 'TimeBoards/add_comment.html', {'form': form})
