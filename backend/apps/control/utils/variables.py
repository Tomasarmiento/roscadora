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

REM_DO_G1 = {
    'contraer_cargador_sup_tras': 1,
    'expandir_cargador_sup_tras': 2,
    'contraer_cargador_inf_tras': 3,
    'expandir_cargador_inf_tras': 4,
    'contraer_brazo_cargador': 5,
    'expandir_brazo_cargador': 6,
    'contraer_brazo_descargador': 7,
    'expandir_brazo_descargador': 8,
    'cerrar_pinza_descargadora': 9,
    'abrir_pinza_descargadora': 10,
    'contraer_cargador_sup_del': 11,
    'empty_1': 12,
    'contraer_cargador_inf_del': 13,
    'empty_2': 14,
    'expandir_vertical_carga': 15,
    'empty_3': 16
}

REM_DO_G2 = {
    'expandir_horiz_pinza_desc': 17,
    'empty_1': 18,
    'contraer_vert_pinza_desc': 19,
    'empty_2': 20,
    'expandir_acople_libric': 21,
    'contraer_clampeo_plato': 22,
    'expandir_clampeo_plato': 23,
    'encender_bomba_hidraulica': 24,
    'encender_bomba_soluble': 25,
    'presurizar':26,
    'cerrar_boquilla_1': 27,
    'abrir_boquilla_1': 28,
    'cerrar_boquilla_2': 29,
    'abrir_boquilla_2': 30,
    'cerrar_boquilla_3': 31,
    'abrir_boquilla_3': 32,
}

REM_DO_G1_ARR = [
    'contraer_cargador_sup_tras',   #1 - 0
    'expandir_cargador_sup_tras',   #2 - 1
    'contraer_cargador_inf_tras',   #3 - 2
    'expandir_cargador_inf_tras',   #4 - 3
    'contraer_brazo_cargador',      #5 - 4
    'expandir_brazo_cargador',      #6 - 5
    'contraer_brazo_descargador',   #7 - 6
    'expandir_brazo_descargador',   #8 - 7
    'cerrar_pinza_descargadora',    #9 - 8
    'abrir_pinza_descargadora',     #10 - 9
    'contraer_cargador_sup_del',    #11 - 10
    '',                             #12 - 11
    'contraer_cargador_inf_del',    #13 - 12
    '',                             #14 - 13
    'expandir_vertical_carga',      #15 - 14
    '',                             #16 - 15
]

REM_DO_G2_ARR = [
    'expandir_horiz_pinza_desc',    #17 - 0
    '',                             #18 - 1
    'contraer_vert_pinza_desc',     #19 - 2
    '',                             #20 - 3
    'expandir_acople_libric',       #21 - 4
    'contraer_clampeo_plato',       #22 - 5
    'expandir_clampeo_plato',       #23 - 6
    'encender_bomba_hidraulica',    #24 - 7
    'encender_bomba_soluble',       #25 - 8
    'presurizar',                   #26 - 9
    'cerrar_boquilla_1',            #27 - 10
    'abrir_boquilla_1',             #28 - 11
    'cerrar_boquilla_2',            #29 - 12
    'abrir_boquilla_2',             #30 - 13
    'cerrar_boquilla_3',            #31 - 14
    'abrir_boquilla_3',             #32 - 15
]

REM_DI_G1 = [
    'cargador_sup_tras_contraido',  # 1 - 0
    'cargador_sup_tras_expandido',  # 2 - 1
    'cargador_inf_tras_contraido',  # 3 - 2
    'cargador_inf_tras_expandido',  # 4 - 3
    'brazo_cargador_contraido',     # 5 - 4
    'brazo_cargador_expandido',     # 6 - 5
    'brazo_descarga_contraido',     # 7 - 6
    'brazo_descarga_expandido',     # 8 - 7
    'pinza_descargadora_cerrada',   # 9 - 8
    'pinza_descargadora_abierta',   # 10 - 9
    'cargadora_sup_del_contraido',  # 11 - 10
    'cargadora_sup_del_expandido',  # 12 - 11
    'cargadora_inf_del_contraido',  # 13 - 12
    'cargadora_inf_del_expandido',  # 14 - 13
    'vertical_carga_contraido',     # 15 - 14
    'vertical_carga_expandido',     # 16 - 15
]

REM_DI_G2 = [
    'horiz_pinza_desc_contraido',   # 17 - 0
    'horiz_pinza_desc_expandido',   # 18 - 1
    'vert_pinza_desc_contraido',    # 19 - 2
    'vert_pinza_desc_expandido',    # 20 - 3
    'acople_libric_contraido',      # 21 - 4
    'acople_libric_expandido',      # 22 - 5
    'clampeo_plato_contraido',      # 23 - 6
    'clampeo_plato_expandido',      # 24 - 7
    'pieza_en_boquilla_1',          # 25 - 8
    'pieza_en_boquilla_2',          # 26 - 9
    'contador_inferior',            # 27 - 10
    '',                             # 28 - 11
    'contador_superior',            # 29 - 12
    '',                             # 30 - 13
    '',                             # 31 - 14
    'baja_presion',                 # 32 - 15
]