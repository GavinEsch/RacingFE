from django import forms
from .models import (LeaderboardEntry, Game, Track, Car, Session, Attempt, TelemetryData, Achievement, Comment, Event, Rating, UserAchievement,User)
from django.contrib.auth.forms import UserCreationForm
from datetime import timedelta
class LeaderboardEntryForm(forms.ModelForm):
    minutes = forms.IntegerField(min_value=0, label="Minutes")
    seconds = forms.IntegerField(min_value=0, max_value=59, label="Seconds")
    milliseconds = forms.IntegerField(min_value=0, max_value=999, label="Milliseconds")

    class Meta:
        model = LeaderboardEntry
        fields = ['user', 'minutes', 'seconds', 'milliseconds']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        minutes = cleaned_data.get('minutes') or 0
        seconds = cleaned_data.get('seconds') or 0
        milliseconds = cleaned_data.get('milliseconds') or 0
        cleaned_data['time'] = timedelta(minutes=minutes, seconds=seconds, milliseconds=milliseconds)
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.time = self.cleaned_data['time']
        if commit:
            instance.save()
        return instance


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'settings']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'settings': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TrackForm(forms.ModelForm):
    cars = forms.ModelMultipleChoiceField(queryset=Car.objects.all(), label='Cars Used for Leaderboard', widget=forms.SelectMultiple(attrs={'class': 'form-select'}))

    class Meta:
        model = Track
        fields = ['name', 'cars', 'configurations', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'configurations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }



class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['user', 'game', 'end_time']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'game': forms.Select(attrs={'class': 'form-select'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }

class AttemptForm(forms.ModelForm):
    class Meta:
        model = Attempt
        fields = ['session', 'track', 'car', 'time']
        widgets = {
            'session': forms.Select(attrs={'class': 'form-select'}),
            'track': forms.Select(attrs={'class': 'form-select'}),
            'car': forms.Select(attrs={'class': 'form-select'}),
            'time': forms.TimeInput(attrs={'class': 'form-control'}),
        }

class TelemetryDataForm(forms.ModelForm):
    class Meta:
        model = TelemetryData
        fields = ['user', 'car', 'track', 'game', 'session', 'speed', 'acceleration', 'lap_time', 'other_data', 'gps_coordinates', 'brake_usage']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'car': forms.Select(attrs={'class': 'form-select'}),
            'track': forms.Select(attrs={'class': 'form-select'}),
            'game': forms.Select(attrs={'class': 'form-select'}),
            'session': forms.Select(attrs={'class': 'form-select'}),
            'speed': forms.NumberInput(attrs={'class': 'form-control'}),
            'acceleration': forms.NumberInput(attrs={'class': 'form-control'}),
            'lap_time': forms.TimeInput(attrs={'class': 'form-control'}),
            'other_data': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'gps_coordinates': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'brake_usage': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class UserAchievementForm(forms.ModelForm):
    class Meta:
        model = UserAchievement
        fields = ['user', 'achievement']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'achievement': forms.Select(attrs={'class': 'form-select'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'content', 'track', 'game', 'car', 'parent']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'track': forms.Select(attrs={'class': 'form-select'}),
            'game': forms.Select(attrs={'class': 'form-select'}),
            'car': forms.Select(attrs={'class': 'form-select'}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'game', 'start_time', 'end_time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'game': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['user', 'track', 'game', 'car', 'rating', 'review']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'track': forms.Select(attrs={'class': 'form-select'}),
            'game': forms.Select(attrs={'class': 'form-select'}),
            'car': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'preferences', 'profile_picture')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'preferences': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['game', 'end_time']
        widgets = {
            'game': forms.Select(attrs={'class': 'form-select'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }