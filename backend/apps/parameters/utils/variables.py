# -------------------------------------------------------------------------------------------- #
# ---------------------------------- Parts parameters ---------------------------------------- #
# -------------------------------------------------------------------------------------------- #

PARAM_NAMES = [
    'paso_de_rosca',
    'posicion_de_aprox',
    'velocidad_de_aprox',
    'distancia_de_roscado',
    'velocidad_de_roscado',
    'velocidad_de_retraccion',
    'tiempo_de_ciclo',
    'torque_tolerado',
    't_inicio_soluble'
]


PARAM_DEFAULT_VALUES_1 = {
    'paso_de_rosca': 0.0,
    'posicion_de_aprox': 0.0,
    'velocidad_de_aprox': 0.0,
    'distancia_de_roscado': 0.0,
    'velocidad_de_roscado': 0.0,
    'velocidad_de_retraccion': 0.0,
    'tiempo_de_ciclo': 0.0,
    'torque_tolerado': 0.0,
    't_inicio_soluble': 0.0,
}

PARAM_DEFAULT_VALUES_2 = {
    'paso_de_rosca': 0.0,
    'posicion_de_aprox': 0.0,
    'velocidad_de_aprox': 0.0,
    'distancia_de_roscado': 0.0,
    'velocidad_de_roscado': 0.0,
    'velocidad_de_retraccion': 0.0,
    'tiempo_de_ciclo': 0.0,
    'torque_tolerado': 0.0,
    't_inicio_soluble': 0.0,
}

PARAM_DEFAULT_VALUES_3 = {
    'paso_de_rosca': 0.0,
    'posicion_de_aprox': 0.0,
    'velocidad_de_aprox': 0.0,
    'distancia_de_roscado': 0.0,
    'velocidad_de_roscado': 0.0,
    'velocidad_de_retraccion': 0.0,
    'tiempo_de_ciclo': 0.0,
    'torque_tolerado': 0.0,
    't_inicio_soluble': 0.0,
}

PARAM_DEFAULT_VALUES = {
    1: PARAM_DEFAULT_VALUES_1,
    2: PARAM_DEFAULT_VALUES_2,
    3: PARAM_DEFAULT_VALUES_3
}

PARAMS_UNITS = {
    'paso_de_rosca': 'mm/v',
    'posicion_de_aprox': 'mm',
    'velocidad_de_aprox': 'mm/seg',
    'distancia_de_roscado': 'mm',
    'velocidad_de_roscado': 'mm/seg',
    'velocidad_de_retraccion': 'mm/seg',
    'tiempo_de_ciclo': 'seg',
    'torque_tolerado': 'Nm',
    't_inicio_soluble': 'seg',
}

SELECTED_MODEL = 1
PART_MODEL_OPTIONS = (1, 2, 3)

PARAMS = {}

# -------------------------------------------------------------------------------------------- #
# ---------------------------------- Routines Parameters ------------------------------------- #
# -------------------------------------------------------------------------------------------- #

HOMING_PARAM_NAMES = [
    'position_positive_7',
    'position_mid_low',
    'position_mid_high',
    'position_negative_7'
]

HOMING_PARAMS_DEFAULT_VALUES = {
    'position_positive_7':  4,
    'position_mid_low':     -3,
    'position_mid_high':    1,
    'position_negative_7':  -4
}