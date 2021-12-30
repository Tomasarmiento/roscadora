from apps.parameters.utils.variables import PARAMS, PARAM_DEFAULT_VALUES, PARAMS_UNITS, SELECTED_MODEL,\
    PART_MODEL_OPTIONS
from django.apps import AppConfig


class ParametersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.parameters'

    def ready(self):
        from .models import Parameter
        params = Parameter.objects.all()
        saved_params = dict([(param.name, param.value) for param in params])
        saved_keys = saved_params.keys()

        for option in PART_MODEL_OPTIONS:
            for key, value in PARAM_DEFAULT_VALUES[option].items():           
                if key not in saved_keys:
                    new_param = Parameter(
                        name = key,
                        value = value,
                        part_model = option,
                        unit = PARAMS_UNITS[key]
                        )
                    new_param.save()
                if option == SELECTED_MODEL:
                    PARAMS[key] = value
