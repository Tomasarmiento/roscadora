from apps.control.utils import variables as ctrl_vars
from . import variables as param_vars
    
    
def init_params():        # params: query with all parameters in database
    from apps.parameters.models import Parameter
    params = Parameter.objects.all()
    saved_params = dict([(param.name, param.value) for param in params])
    saved_keys = saved_params.keys()

    for option in param_vars.PART_MODEL_OPTIONS:
        f_params = params.filter(part_model=option)
        f_saved_params = dict([(param.name, param.value) for param in f_params])
        f_saved_keys = f_saved_params.keys()
        for key, value in param_vars.PARAM_DEFAULT_VALUES[option].items():           
            if key not in f_saved_keys:
                Parameter.objects.create(
                    name = key,
                    value = value,
                    part_model = option,
                    unit = param_vars.PARAMS_UNITS.get(key, '')
                    )
            
            if option == param_vars.SELECTED_MODEL:
                param_vars.PARAMS[key] = value
    
    for homing_param_name in param_vars.HOMING_PARAM_NAMES:
        if homing_param_name not in saved_keys:
            Parameter.objects.create(
                name = homing_param_name,
                value = param_vars.HOMING_PARAMS_DEFAULT_VALUES[homing_param_name],
                part_model = 0
            )
        ctrl_vars.HOMING_CONSTANTES[homing_param_name] = params.get(name=homing_param_name)
    
    update_roscado_params()


def update_homing_params():
    from apps.parameters.models import Parameter
    params = Parameter.objects.all()
    for homing_param_name in param_vars.HOMING_PARAM_NAMES:
        ctrl_vars.HOMING_CONSTANTES[homing_param_name] = params.filter(part_model=0).get(name=homing_param_name)

def update_roscado_params():
    from apps.parameters.models import Parameter
    params = Parameter.objects.all()
    part_model = param_vars.SELECTED_MODEL
    for roscado_param_name in param_vars.ROSCADO_PARAMS_NAMES:
        param = params.filter(part_model=part_model).get(name=roscado_param_name)
        # param.value = param_vars.ROSCADO_PARAMS_PARAMS_DEFAULT_VALUES[roscado_param_name]
        # param.save()
        ctrl_vars.ROSCADO_CONSTANTES[roscado_param_name] = int(param.value)