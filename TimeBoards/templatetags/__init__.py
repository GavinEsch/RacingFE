# in apps.py
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'TimeBoards'

    def ready(self):
        import TimeBoards.templatetags.json_extras
