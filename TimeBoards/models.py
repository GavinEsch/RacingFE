from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta, datetime

class User(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    preferences = models.JSONField(default=dict, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='timeboards_user_set',  # Custom related_name
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='timeboards_user_set',  # Custom related_name
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_query_name='user',
    )

    def __str__(self):
        return self.username

class Game(models.Model):
    name = models.CharField(max_length=100)
    settings = models.JSONField(default=dict)

    def __str__(self):
        return self.name

class Track(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    configurations = models.JSONField(default=dict)
    image = models.ImageField(upload_to='track_images/', null=True, blank=True)
    cars = models.ManyToManyField('Car', related_name='tracks', blank=True)

    def __str__(self):
        return self.name

class Car(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.game.name} - {self.start_time}"


class Attempt(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    time = models.DurationField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set on creation

    def __str__(self):
        return f"{self.session.user.username} - {self.track.name} - {self.timestamp}"

class LeaderboardEntry(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
        if self.pk:
            orig = LeaderboardEntry.objects.get(pk=self.pk)
            if orig.time != self.time:
                self.logged_at = datetime.now()
        super().save(*args, **kwargs)

    @property
    def formatted_time(self):
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
        return "00:00:000"

    @staticmethod
    def format_duration(duration):
        if not duration:
            return "00:00:000"
        total_seconds = int(duration.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        milliseconds = duration.microseconds // 1000
        return f"{minutes:02}:{seconds:02}:{milliseconds:03}"

class TelemetryData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)  # Link to the session
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    speed = models.FloatField(help_text="Average speed for the lap")  # Average speed for the lap
    acceleration = models.FloatField()
    lap_time = models.DurationField()
    other_data = models.JSONField(default=dict)
    gps_coordinates = models.JSONField(default=dict, help_text="GPS coordinates during the lap")
    brake_usage = models.FloatField(help_text="Percentage of brake usage during the lap")

    class Meta:
        indexes = [
            models.Index(fields=['user', 'car', 'track', 'game']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.car.name} - {self.track.name} - {self.game.name}"

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    users = models.ManyToManyField(User, through='UserAchievement')

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_awarded = models.DateTimeField(auto_now_add=True)  # Automatically set on creation

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    track = models.ForeignKey(Track, on_delete=models.CASCADE, null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message}"

class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"

class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_of', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user.username} is friends with {self.friend.username}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    review = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'track', 'game', 'car')

    def __str__(self):
        return f"{self.user.username} rated {self.rating}"
