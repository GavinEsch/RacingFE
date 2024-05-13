from django.shortcuts import render
from .models import LeaderboardEntry, Track, Car

def homepage(request):
    # Fetching the fastest times for each track and car combination
    entries = LeaderboardEntry.objects.all().select_related('track', 'car').order_by('track', 'car', 'time')[:10]
    return render(request, 'TimeBoards/homepage.html', {'entries': entries})

def track_leaderboard(request, track_id):
    # Fetching the fastest times for a specific track
    entries = LeaderboardEntry.objects.filter(track_id=track_id).select_related('car').order_by('time')[:10]
    track = Track.objects.get(id=track_id)
    return render(request, 'TimeBoards/track_leaderboard.html', {'track': track, 'entries': entries})

def car_leaderboard(request, car_id):
    # Fetching the fastest times for a specific car across all tracks
    entries = LeaderboardEntry.objects.filter(car_id=car_id).select_related('track').order_by('time')[:10]
    car = Car.objects.get(id=car_id)
    return render(request, 'TimeBoards/car_leaderboard.html', {'car': car, 'entries': entries})

from django.shortcuts import redirect
from .forms import LeaderboardEntryForm

def add_leaderboard_entry(request):
    if request.method == 'POST':
        form = LeaderboardEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')  # Adjust the redirect as necessary
    else:
        form = LeaderboardEntryForm()
    return render(request, 'add_leaderboard_entry.html', {'form': form})

def create_leaderboard_entry(request):
    if request.method == 'POST':
        form = LeaderboardEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            # Assuming the form has fields for minutes, seconds, and milliseconds
            entry.set_time_components(
                form.cleaned_data['minutes'],
                form.cleaned_data['seconds'],
                form.cleaned_data['milliseconds']
            )
            entry.save()
            return redirect('homepage')
    else:
        form = LeaderboardEntryForm()
    return render(request, 'TimeBoards/add_leaderboard_entry.html', {'form': form})