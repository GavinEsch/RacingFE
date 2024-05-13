from django.db import models
from datetime import timedelta

class Game(models.Model):
    name = models.CharField(max_length=100)
    settings = models.JSONField(default=dict)  # To store game-specific settings like difficulty levels

class Track(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

class Car(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

class LeaderboardEntry(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)  # Or link to your User model if authentication is involved
    time = models.DurationField()

    class Meta:
        unique_together = ('track', 'car', 'user')
        indexes = [
            models.Index(fields=['track', 'car', 'user']),
            models.Index(fields=['track', 'car']),
        ]

    def set_time_components(self, minutes, seconds, milliseconds):
        """Set the time from separate components and store as a timedelta."""
        self.time = timedelta(minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))
        self.save()  # Ensures the model instance is updated in the database
        
    @property
    def next_closest_time(self):
        # Query to get the next best time that isn't this entry's time
        next_time = LeaderboardEntry.objects.filter(
            track=self.track,
            car=self.car
        ).exclude(id=self.id).order_by('time').first()
        return next_time.time if next_time else None

    @property
    def difference(self):
        next_time = self.next_closest_time
        return next_time - self.time if next_time else timedelta(0)

    @property
    def formatted_time(self):
        """Returns the time as a formatted string."""
        return self.format_duration(self.time)

    @staticmethod
    def format_duration(duration):
        """Converts timedelta to a formatted string."""
        print(duration)
        if not duration:
            return "00:00:000"
        total_seconds = int(duration.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        milliseconds = duration.microseconds // 1000
        return f"{minutes:02}:{seconds:02}:{milliseconds:03}"
