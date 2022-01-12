from django.apps import AppConfig
from apps.control.utils import functions

class ControlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.control'

    def ready(self) -> None:
        from apps.control.models import RoutineInfo
        functions.init_routine_info(RoutineInfo)
        functions.init_rem_io()
        functions.init_comands_ref_rates()
