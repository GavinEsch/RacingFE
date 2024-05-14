# models.py

from django.db import models
from datetime import timedelta, datetime

class Person(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=100)
    settings = models.JSONField(default=dict)  # To store game-specific settings like difficulty levels

    def __str__(self):
        return self.name

class Track(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Car(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class LeaderboardEntry(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    time = models.DurationField()
    logged_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('track', 'car', 'user')
        indexes = [
            models.Index(fields=['track', 'car', 'user']),
            models.Index(fields=['track', 'car']),
        ]

    def set_time_components(self, minutes, seconds, milliseconds):
        new_time = timedelta(minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))
        if not self.time or new_time < self.time:
            self.time = new_time
            self.save()

    def save(self, *args, **kwargs):
        # Update the logged_at field if the time field is changed
        if self.pk:
            orig = LeaderboardEntry.objects.get(pk=self.pk)
            if orig.time != self.time:
                self.logged_at = datetime.now()
        super().save(*args, **kwargs)

    @property
    def formatted_time(self):
        """Returns the time as a formatted string using the static method."""
        return LeaderboardEntry.format_duration(self.time)

    @property
    def next_closest_time(self):
        next_time = LeaderboardEntry.objects.filter(
            track=self.track,
            car=self.car,
            game=self.game
        ).exclude(id=self.id).order_by('time').first()
        return next_time.time if next_time else None

    @property
    def difference(self):
        next_time = self.next_closest_time
        if next_time:
            return LeaderboardEntry.format_duration(abs(next_time - self.time))
        return "00:00:000"  # Return a default formatted string for no difference

    @staticmethod
    def format_duration(duration):
        """Converts timedelta to a formatted string."""
        if not duration:
            return "00:00:000"
        total_seconds = int(duration.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        milliseconds = duration.microseconds // 1000
        return f"{minutes:02}:{seconds:02}:{milliseconds:03}"
