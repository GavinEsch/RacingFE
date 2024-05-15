from django.contrib import admin
from .models import Game, Track, Car, LeaderboardEntry, Person


class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_settings')

    def display_settings(self, obj):
        return ", ".join([f"{k}: {v}" for k, v in obj.settings.items()])
    display_settings.short_description = 'Settings'


class TrackAdmin(admin.ModelAdmin):
    list_display = ('name', 'game')

#caradmin
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'game')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name',)


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

admin.site.register(Game, GameAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(LeaderboardEntry, LeaderboardEntryAdmin)
