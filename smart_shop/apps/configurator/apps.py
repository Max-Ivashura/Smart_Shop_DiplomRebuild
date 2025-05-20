from django.apps import AppConfig


class ConfiguratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.configurator'

    def ready(self):
        import apps.configurator.signals  # Активируем сигналы
