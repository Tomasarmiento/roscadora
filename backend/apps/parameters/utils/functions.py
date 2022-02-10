from .variables import PARAMS, PARAM_DEFAULT_VALUES, PARAMS_UNITS, SELECTED_MODEL,\
    PART_MODEL_OPTIONS, HOMING_PARAM_NAMES, HOMING_PARAMS_DEFAULT_VALUES
    
    
def init_params():        # params: query with all parameters in database
    from apps.parameters.models import Parameter
    params = Parameter.objects.all()
    saved_params = dict([(param.name, param.value) for param in params])
    saved_keys = saved_params.keys()

    for option in PART_MODEL_OPTIONS:
        for key, value in PARAM_DEFAULT_VALUES[option].items():           
            if key not in saved_keys:
                Parameter.objects.create(
                    name = key,
                    value = value,
                    part_model = option,
                    unit = PARAMS_UNITS[key]
                    )
            
            if option == SELECTED_MODEL:
                PARAMS[key] = value
    
    for homing_param_name in HOMING_PARAM_NAMES:
        if homing_param_name not in saved_keys:
            Parameter.objects.create(
                name = homing_param_name,
                value = HOMING_PARAMS_DEFAULT_VALUES[homing_param_name],
                part_model = 0
            )