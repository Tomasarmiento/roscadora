from django.apps import AppConfig
from apps.control.utils.functions import init_rem_io


class ControlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.control'

    def ready(self) -> None:
        init_rem_io()
