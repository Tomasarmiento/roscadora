from apps.service.acdp.messages_app import AcdpAxisMovementEnums

COMMAND_DEFAULT_VALUES = {
    'vel_giro': 360.0,
    'vel_avance': 5.0,
    'vel_carga': 180.0
}

AXIS_IDS = {
    'avance': AcdpAxisMovementEnums.ID_X_EJE_AVANCE,
    'carga': AcdpAxisMovementEnums.ID_X_EJE_CARGA,
    'giro': AcdpAxisMovementEnums.ID_X_EJE_GIRO,
    'axis_amount': AcdpAxisMovementEnums.CANT_EJES
}

COMMAND_REF_RATES = {}

# -------------------------------------------------------------------------------------------- #
# --------------------------------------- Routines ------------------------------------------- #
# -------------------------------------------------------------------------------------------- #

ROUTINE_IDS = {
    'cerado':   1,
    'carga':    2,
    'descarga': 3,
    'cabezal_indexar': 4,
    'roscado':  5
}

ROUTINE_NAMES = [
    'cerado',
    'carga',
    'descarga',
    'roscado'
]

ROSCADO_CONSTANTES = {
    'posicion_de_aproximacion': -20,
    'velocidad_en_vacio': 10,
    'posicion_final_de_roscado': -110,
    'velocidad_de_roscado': 4,
    'posicion_salida_de_roscado': -20,
    'velocidad_de_retraccion': 10,
    'paso_de_rosca': 2.54,
    'posicion_de_inicio': 5,
}

HOMING_CONSTANTES = {
    'position_positive_7': 4,
    'position_mid_low': -3,
    'position_mid_high': 1,
    'position_negative_7': -4,
}

LOAD_STEPS = [
    0,
    -120,
    -240,
    -360,
    -480,
    480,
    360,
    240,
    120
]

BOQUILLA_CARGADOR = {
    0: 2,
    1: 3,
    2: 1,
    3: 2,
    4: 3,
    5: 1,
    6: 2,
    7: 3,
    8: 1,
    9: 2
}

BOQUILLA_DESCARGADOR = {
    0: 3,
    1: 1,
    2: 2,
    3: 3,
    4: 1,
    5: 2,
    6: 3,
    7: 1,
    8: 2,
    9: 3
}

BOQUILLA_ROSCADO = {
    0: 1,
    1: 2,
    2: 3,
    3: 1,
    4: 2,
    5: 3,
    6: 1,
    7: 2,
    8: 3,
    9: 1
}

# -------------------------------------------------------------------------------------------- #
# --------------------------------- Remote/Local outputs ------------------------------------- #
# -------------------------------------------------------------------------------------------- #

LOC_DI_STATES = {}

LOC_DO_STATES = {}

REM_DO_G1_STATES = {}

REM_DO_G2_STATES = {}

REM_DI_G1_STATES = {}

REM_DI_G2_STATES = {}


LOC_DI_BITS = {
    'em_stop':      0,
    'fast_stop':    1
}

LOC_DO_BITS = {
    'em_stop':      0,
    'mask_ctrl_ok': 1,
    'mask_running': 2
}


REM_DO_G1_BITS = {
    'contraer_puntera_descarga':    0,      # Horizontal descarga (Atras: 2-off y 1-on / Adelante: 2-on y 1-off)
    'expandir_puntera_descarga':    1,      # Horizontal descarga (Atras: 2-off y 1-on / Adelante: 2-on y 1-off)
    'contraer_puntera_carga':       2,      # Horizontal carga (Atras: 4-off y 3-on / Adelante: 4-on y 3-off)
    'expandir_puntera_carga':       3,      # Horizontal carga
    'contraer_brazo_cargador':      4,      # Giro carga (Arriba: 6-off y 5-on / Abajo: 6-on y 5-off)
    'expandir_brazo_cargador':      5,      # Giro carga (Arriba: 6-off y 5-on / Abajo: 6-on y 5-off)
    'contraer_brazo_descargador':   6,      # Giro descarga (Arriba: 8-off y 7-on / Abajo: 8-on y 7-off)
    'expandir_brazo_descargador':   7,      # Giro descarga (Arriba: 8-off y 7-on / Abajo: 8-on y 7-off)
    'cerrar_pinza_descargadora':    8,      # Gripper Descarga (Cierra: 10-off y 9-on / Abre: 10-on y 9-off)
    'abrir_pinza_descargadora':     9,      # Gripper Descarga (Cierra: 10-off y 9-on / Abre: 10-on y 9-off)
    'contraer_boquilla_descarga':   10,     # Boquilla Descarga (Cierra: 11-on / Abre: 11-off)
                                            # 11 not implemented
    'contraer_boquilla_carga':      12,     # Boquilla Carga (Cierra: 13-on / Abre: 13-off)
                                            # 13 not implemented
    'expandir_vertical_carga':      14,     # Vertical Carga (Arriba: 15-on / Abajo: 15-off)
                                            # 15 not implemented
}

REM_DO_G2_BITS = {
    'expandir_horiz_pinza_desc':    0,      # Horizon Gripper descarga (Adelante: 17-off / Atras: 17-on)
                                            # 1 not implemented
    'expandir_vert_pinza_desc':     2,      # Vertical Gripper descarga (Arriba: 19-off / Abajo: 19-on)
                                            # 3 not implemented
    'expandir_acople_lubric':       4,      # Acopla Soluble (SI: 21-on / NO: 21-off)
    'contraer_clampeo_plato':       5,      # Clampeo (SI: 22-off y 23-on / NO: 22-on y 23-off)
    'expandir_clampeo_plato':       6,      # Clampeo (SI: 22-off y 23-on / NO: 22-on y 23-off)
    'encender_bomba_hidraulica':    7,      # Bomba Hidraulica (ON: 24-on / OFF: 24-off)
    'encender_bomba_soluble':       8,      # Bomba Soluble (ON: 25-on / OFF: 25-off)
    'presurizar':                   9,      # Presión (SI: 26-on / NO: 26-off)
    'cerrar_boquilla_1':            10,     # Boquilla 1 (Cierra: 28-off y 27-on / Abre: 28-on y 27-off)
    'abrir_boquilla_1':             11,     # Boquilla 1 (Cierra: 28-off y 27-on / Abre: 28-on y 27-off)
    'cerrar_boquilla_2':            12,     # Boquilla 2 (Cierra: 30-off y 29-on / Abre: 30-on y 29-off)
    'abrir_boquilla_2':             13,     # Boquilla 2 (Cierra: 30-off y 29-on / Abre: 30-on y 29-off)
    'cerrar_boquilla_3':            14,     # Boquilla 3 (Cierra: 32-off y 31-on / Abre: 32-on y 31-off)
    'abrir_boquilla_3':             15      # Boquilla 3 (Cierra: 32-off y 31-on / Abre: 32-on y 31-off)
}

REM_DI_G1_BITS = {
    'puntera_descarga_contraida':   0,
    'puntera_descarga_expandida':   1,
    'puntera_carga_contraida':      2,
    'puntera_carga_expandida':      3,
    'brazo_cargador_contraido':     4,
    'brazo_cargador_expandido':     5,
    'brazo_descarga_contraido':     6,
    'brazo_descarga_expandido':     7,
    'pinza_descargadora_cerrada':   8,
    'pinza_descargadora_abierta':   9,
    'boquilla_descarga_contraida':  10,
    'boquilla_descarga_expandida':  11,
    'boquilla_carga_contraida':     12,
    'boquilla_carga_expandida':     13,
    'vertical_carga_contraido':     14,
    'vertical_carga_expandido':     15,
}

REM_DI_G2_BITS = {
    'horiz_pinza_desc_contraido':   0,
    'horiz_pinza_desc_expandido':   1,
    'vert_pinza_desc_contraido':    2,
    'vert_pinza_desc_expandido':    3,
    'acople_lubric_contraido':      4,
    'acople_lubric_expandido':      5,
    'clampeo_plato_contraido':      6,
    'clampeo_plato_expandido':      7,
    'pieza_en_boquilla_descarga':   8,
    'pieza_en_boquilla_carga':      9,
    'presencia_cupla_en_cargador':  10,
                                    # 11 not implemented
    'cupla_por_tobogan_descarga':   12,
                                    # 13 not implemented
                                    # 14 not implemented
    'presion_normal':               15,
}


LOC_DI_ARR = [
    'em_stop',
    'fast_stop'
]

LOC_DO_ARR = [
    'em_stop',
    'mask_ctrl_ok',
    'mask_running'
]


REM_DO_G1_ARR = [
    'contraer_puntera_descarga',    # 1 - 0
    'expandir_puntera_descarga',    # 2 - 1
    'contraer_puntera_carga',       # 3 - 2
    'expandir_puntera_carga',       # 4 - 3
    'contraer_brazo_cargador',      # 5 - 4
    'expandir_brazo_cargador',      # 6 - 5
    'contraer_brazo_descargador',   # 7 - 6
    'expandir_brazo_descargador',   # 8 - 7
    'cerrar_pinza_descargadora',    # 9 - 8
    'abrir_pinza_descargadora',     # 10 - 9
    'contraer_boquilla_descarga',   # 11 - 10
    '',                             # 12 - 11
    'contraer_boquilla_carga',      # 13 - 12
    '',                             # 14 - 13
    'expandir_vertical_carga',      # 15 - 14
    '',                             # 16 - 15
]

REM_DO_G2_ARR = [
    'expandir_horiz_pinza_desc',    #17 - 0
    '',                             #18 - 1
    'expandir_vert_pinza_desc',     #19 - 2
    '',                             #20 - 3
    'expandir_acople_lubric',       #21 - 4
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

REM_DI_G1_ARR = [
    'puntera_descarga_contraida',  # 1 - 0
    'puntera_descarga_expandida',  # 2 - 1
    'puntera_carga_contraida',      # 3 - 2
    'puntera_carga_expandida',      # 4 - 3
    'brazo_cargador_contraido',     # 5 - 4
    'brazo_cargador_expandido',     # 6 - 5
    'brazo_descarga_contraido',     # 7 - 6
    'brazo_descarga_expandido',     # 8 - 7
    'pinza_descargadora_cerrada',   # 9 - 8
    'pinza_descargadora_abierta',   # 10 - 9
    'boquilla_descarga_contraida',  # 11 - 10
    'boquilla_descarga_expandida',  # 12 - 11
    'boquilla_carga_contraida',     # 13 - 12
    'boquilla_carga_expandida',     # 14 - 13
    'vertical_carga_contraido',     # 15 - 14
    'vertical_carga_expandido',     # 16 - 15
]

REM_DI_G2_ARR = [
    'horiz_pinza_desc_contraido',   # 17 - 0
    'horiz_pinza_desc_expandido',   # 18 - 1
    'vert_pinza_desc_contraido',    # 19 - 2
    'vert_pinza_desc_expandido',    # 20 - 3
    'acople_lubric_contraido',      # 21 - 4
    'acople_lubric_expandido',      # 22 - 5
    'clampeo_plato_contraido',      # 23 - 6
    'clampeo_plato_expandido',      # 24 - 7
    'pieza_en_boquilla_descarga',   # 25 - 8
    'pieza_en_boquilla_carga',      # 26 - 9
    'presencia_cupla_en_cargador',  # 27 - 10
    '',                             # 28 - 11
    'cupla_por_tobogan_descarga',   # 29 - 12
    '',                             # 30 - 13
    '',                             # 31 - 14
    'presion_normal',               # 32 - 15
]