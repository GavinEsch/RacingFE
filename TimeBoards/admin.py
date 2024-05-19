from django.contrib import admin
from .models import (User, Game, Track, Car, Session, Attempt, LeaderboardEntry, TelemetryData, Achievement, UserAchievement, Comment, Notification, Log, Event, Message, Friendship, Rating)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'bio')

class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_settings')

    def display_settings(self, obj):
        return ", ".join([f"{k}: {v}" for k, v in obj.settings.items()])
    display_settings.short_description = 'Settings'

class TrackAdmin(admin.ModelAdmin):
    list_display = ('name', 'game')

class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'game')

class SessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'start_time', 'end_time')

class AttemptAdmin(admin.ModelAdmin):
    list_display = ('session', 'track', 'car', 'time', 'timestamp')

class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ('track', 'car', 'user', 'formatted_time', 'display_next_closest_time', 'display_difference')

    def formatted_time(self, obj):
        return obj.formatted_time
    formatted_time.short_description = 'Time'

    def display_next_closest_time(self, obj):
        next_time = obj.next_closest_time
        return obj.format_duration(next_time) if next_time else 'N/A'
    display_next_closest_time.short_description = 'Next Closest Time'

    def display_difference(self, obj):
        difference = obj.difference
        return obj.format_duration(difference) if difference else 'N/A'
    display_difference.short_description = 'Difference'

class TelemetryDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'track', 'game', 'session', 'timestamp', 'speed', 'acceleration', 'lap_time')

class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'date_awarded')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'track', 'game', 'car', 'created_at')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'read', 'created_at')

class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'created_at')

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'game', 'start_time', 'end_time')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp')

class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend', 'created_at')

class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'game', 'car', 'rating', 'created_at', 'review')

admin.site.register(User, UserAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Attempt, AttemptAdmin)
admin.site.register(LeaderboardEntry, LeaderboardEntryAdmin)
admin.site.register(TelemetryData, TelemetryDataAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(UserAchievement, UserAchievementAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Friendship, FriendshipAdmin)
admin.site.register(Rating, RatingAdmin)
