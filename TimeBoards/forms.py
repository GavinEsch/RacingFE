# forms.py

from django import forms
from .models import LeaderboardEntry, Person, Game
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
        fields = ['name', 'settings']  # Adjust fields as necessary
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'settings': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

class AddTrackForm(forms.Form):
    track_name = forms.CharField(label='Track Name', max_length=100)
    car_name = forms.CharField(label='Car Name', max_length=100)

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name']