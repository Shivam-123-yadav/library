from django.apps import AppConfig

class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'
# apps.py (inside your app e.g. library/apps.py)
def ready(self):
    import library.signals
