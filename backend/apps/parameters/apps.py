from apps.parameters.utils.functions import init_params
from django.apps import AppConfig


class ParametersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.parameters'

    def ready(self):
        from .models import Parameter
        init_params(Parameter)
        # saved_params = dict([(param.name, param.value) for param in params])
        # saved_keys = saved_params.keys()

        # for option in PART_MODEL_OPTIONS:
        #     for key, value in PARAM_DEFAULT_VALUES[option].items():           
        #         if key not in saved_keys:
        #             new_param = Parameter(
        #                 name = key,
        #                 value = value,
        #                 part_model = option,
        #                 unit = PARAMS_UNITS[key]
        #                 )
        #             new_param.save()
        #         if option == SELECTED_MODEL:
        #             PARAMS[key] = value
