# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import LeaderboardEntry, Track, Car, Game, Person
from .forms import LeaderboardEntryForm
from datetime import timedelta

def homepage(request):
    # Fetching the fastest time for each track and car combination
    entries = LeaderboardEntry.objects.all().select_related('track', 'car', 'game').order_by('track', 'car', 'time')
    top_times = {}

    for entry in entries:
        key = (entry.track, entry.car, entry.game)
        if key not in top_times:
            top_times[key] = entry

    return render(request, 'TimeBoards/homepage.html', {'entries': top_times.values()})

def track_leaderboard(request, track_id, car_id):
    # Fetching the fastest times for a specific track and car combination
    entries = LeaderboardEntry.objects.filter(track_id=track_id, car_id=car_id).select_related('car', 'game').order_by('time')[:10]
    track = Track.objects.get(id=track_id)
    car = Car.objects.get(id=car_id)
    return render(request, 'TimeBoards/track_leaderboard.html', {'track': track, 'car': car, 'entries': entries})

def car_leaderboard(request, car_id):
    # Fetching the fastest times for a specific car across all tracks
    entries = LeaderboardEntry.objects.filter(car_id=car_id).select_related('track', 'game').order_by('time')[:10]
    car = Car.objects.get(id=car_id)
    return render(request, 'TimeBoards/car_leaderboard.html', {'car': car, 'entries': entries})

def add_leaderboard_entry(request):
    if request.method == 'POST':
        form = LeaderboardEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')  # Adjust the redirect as necessary
    else:
        form = LeaderboardEntryForm()
    return render(request, 'TimeBoards/add_leaderboard_entry.html', {'form': form})

def track_times(request, game_id, track_id, car_id):
    game = get_object_or_404(Game, id=game_id)
    track = get_object_or_404(Track, id=track_id, game=game)
    car = get_object_or_404(Car, id=car_id, game=game, track=track)
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
        form = LeaderboardEntryForm()

    return render(request, 'TimeBoards/track_times.html', {'game': game, 'track': track, 'car': car, 'times': times, 'form': form})

def games(request):
    all_games = Game.objects.all()
    return render(request, 'TimeBoards/games.html', {'games': all_games})

def tracks(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    tracks = Track.objects.filter(game=game)
    tracks_with_cars = []
    for track in tracks:
        cars = Car.objects.filter(game=game, track=track)
        for car in cars:
            tracks_with_cars.append((track, car))
    return render(request, 'TimeBoards/tracks.html', {'game': game, 'tracks_with_cars': tracks_with_cars})

def people(request):
    all_people = Person.objects.all()
    return render(request, 'TimeBoards/people.html', {'people': all_people})

def person_times(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    times = LeaderboardEntry.objects.filter(user=person).order_by('time')
    return render(request, 'TimeBoards/person_times.html', {'person': person, 'times': times})
