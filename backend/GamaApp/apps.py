from django.apps import AppConfig

class GamaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GamaApp'

    def ready(self):
        import GamaApp.signals  # Conectar la señal
