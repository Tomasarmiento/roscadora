from apps.parameters.utils.variables import PARAMS, PARAMS_DEFAULT_VALUES, PARAMS_UNITS, SELECTED_MODEL
from django.apps import AppConfig


class ParametersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.parameters'

    def ready(self):
        from .models import Parameter
        params = Parameter.objects.all()
        saved_params = dict([(param.name, param.value) for param in params])
        saved_keys = saved_params.keys()

        for key, value in PARAMS_DEFAULT_VALUES.items():           
            if key not in saved_keys:
                PARAMS[key] = value
                new_param = Parameter(name=key, value=value, part_model=SELECTED_MODEL, unit=PARAMS_UNITS[key])
                new_param.save()
            else:
                PARAMS[key] = saved_params[key]
