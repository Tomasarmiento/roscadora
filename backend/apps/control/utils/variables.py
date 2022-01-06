from apps.service.acdp.messages_app import AcdpAxisMovementEnums

COMMAND_DEFAULT_VALUES = {
    'vel_eje_giro': 360.0,
    'vel_eje_avance': 5.0,
    'vel_eje_carga': 180.0
}


AXIS_IDS = {
    'avance': AcdpAxisMovementEnums.ID_X_EJE_AVANCE,
    'carga': AcdpAxisMovementEnums.ID_X_EJE_CARGA,
    'giro': AcdpAxisMovementEnums.ID_X_EJE_GIRO
}