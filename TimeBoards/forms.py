from django import forms
from .models import LeaderboardEntry, Track, Car
from datetime import timedelta

from django import forms
from .models import LeaderboardEntry

# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import LeaderboardEntry
from datetime import timedelta

class LeaderboardEntryForm(forms.ModelForm):
    minutes = forms.IntegerField(min_value=0, label="Minutes")
    seconds = forms.IntegerField(min_value=0, max_value=59, label="Seconds")
    milliseconds = forms.IntegerField(min_value=0, max_value=999, label="Milliseconds")

    class Meta:
        model = LeaderboardEntry
        fields = ['track', 'car', 'user', 'minutes', 'seconds', 'milliseconds']
        widgets = {
            'track': forms.Select(attrs={'class': 'form-select'}),
            'car': forms.Select(attrs={'class': 'form-select'}),
            'user': forms.TextInput(attrs={'class': 'form-control'})
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

