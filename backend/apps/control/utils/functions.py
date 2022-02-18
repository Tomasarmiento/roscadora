import django
import random, time
from datetime import datetime
from apps.service.acdp.handlers import build_msg
from apps.service.api.variables import Commands, COMMANDS
from apps.service.acdp import messages_app as msg_app
from apps.service.acdp import messages_base as msg_base

from apps.control.utils import variables as ctrl_vars

from apps.ws.utils.handlers import send_message
from apps.ws.utils.functions import send_front_message, get_ch_info
from apps.ws.utils import variables as ws_vars


# -------------------------------------------------------------------------------------------- #
# ----------------------------------- Initialization ----------------------------------------- #
# -------------------------------------------------------------------------------------------- #

def init_rem_io():
    for i in range(len(ctrl_vars.REM_DI_G1_ARR)):
        key = ctrl_vars.REM_DI_G1_ARR[i]
        if key: ctrl_vars.REM_DI_G1_STATES[key] = None
        key = ctrl_vars.REM_DI_G2_ARR[i]
        if key: ctrl_vars.REM_DI_G2_STATES[key] = None
        key = ctrl_vars.REM_DO_G1_ARR[i]
        if key: ctrl_vars.REM_DO_G1_STATES[key] = None
        key = ctrl_vars.REM_DO_G2_ARR[i]
        if key: ctrl_vars.REM_DO_G2_STATES[key] = None


def init_loc_io():
    for key in ctrl_vars.LOC_DI_ARR:
        ctrl_vars.LOC_DI_STATES[key] = None
    for key in ctrl_vars.LOC_DO_ARR:
        ctrl_vars.LOC_DO_STATES[key] = None


def init_routine_info():
    from apps.control.models import RoutineInfo
    routines = RoutineInfo.objects.all()
    rtn_names = []
    for routine in routines:
        rtn_names.append(routine.name)
        routine.running = 0
        routine.save()
    for rtn_name in ctrl_vars.ROUTINE_NAMES.values():
        if rtn_name not in rtn_names:
            RoutineInfo.objects.create(name=rtn_name, running=0)


def init_comands_ref_rates():
    for key, value in ctrl_vars.COMMAND_DEFAULT_VALUES.items():
        ctrl_vars.COMMAND_REF_RATES[key] = value


def init_master_flags():
    ws_vars.MicroState.master_running = False
    ws_vars.MicroState.master_stop = False
    ws_vars.MicroState.iteration = 0

# -------------------------------------------------------------------------------------------- #
# --------------------------------------- Routines ------------------------------------------- #
# -------------------------------------------------------------------------------------------- #



# ********* condiciones iniciales - MASTER *********
def check_init_conditions_master():
    
    if ws_vars.MicroState.rem_i_states[1]['presion_normal'] == False:
        err_msg = 'Baja presión'
        print('\nBaja presión\n')
        ws_vars.MicroState.err_messages.append(err_msg)
        return False

    pos = round(ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['carga']]['pos_fil'], 0)
    if pos not in ctrl_vars.LOAD_STEPS:
        err_msg = 'Error en posicion de cabezal' 
        print('\nError en posicion de cabezal\n')
        ws_vars.MicroState.err_messages.append(err_msg)
        return False

    err_msg_index = check_init_conditions_index()
    err_msg_load = check_init_conditions_load()
    err_msg_unload = check_init_conditions_unload()
    err_msg_tapping = check_init_conditions_tapping()
    error_flag = False
    
    if err_msg_load:
        print('\nError en condiciones iniciales de carga')
        err_msg = 'Error en condiciones iniciales de carga'
        ws_vars.MicroState.err_messages.append(err_msg)
        for err in err_msg_load:
            ws_vars.MicroState.err_messages.append(err)
            print(err)
        error_flag = True
    else:
        log_msg = 'Condiciones iniciales de carga OK'
        print('Condiciones iniciales de carga OK')
        ws_vars.MicroState.log_messages.append(log_msg)
    
    if err_msg_unload:
        print('\nError en condiciones iniciales de descarga')
        err_msg = 'Error en condiciones iniciales de descarga'
        ws_vars.MicroState.err_messages.append(err_msg)
        for err in err_msg_unload:
            ws_vars.MicroState.err_messages.append(err)
            print(err)
        error_flag = True
    else:
        log_msg = 'Condiciones iniciales de descarga OK'
        print('Condiciones iniciales de descarga OK')
        ws_vars.MicroState.log_messages.append(log_msg)
    
    if err_msg_index:
        print('\nError en condiciones iniciales de indexado')
        err_msg = 'Error en condiciones iniciales de indexado'
        ws_vars.MicroState.err_messages.append(err_msg)
        for err in err_msg_index:
            ws_vars.MicroState.err_messages.append(err)
            print(err)
        error_flag = True
    else:
        log_msg = 'Condiciones iniciales de indexado OK'
        print('Condiciones iniciales de indexado OK')
        ws_vars.MicroState.log_messages.append(log_msg)
    
    if err_msg_tapping:
        print('\nError en condiciones iniciales de roscado')
        err_msg = 'Error en condiciones iniciales de roscado'
        ws_vars.MicroState.err_messages.append(err_msg)
        for err in err_msg_tapping:
            ws_vars.MicroState.err_messages.append(err)
            print(err)
        error_flag = True
    else:
        log_msg = 'Condiciones iniciales de roscado OK'
        print('Condiciones iniciales de roscado OK')
        ws_vars.MicroState.log_messages.append(log_msg)

    if error_flag == True:
        return False
    return True



# ********* condiciones iniciales - HOMING *********
def check_init_conditions_homing():
    eje_avance = ctrl_vars.AXIS_IDS['avance']
    eje_carga = ctrl_vars.AXIS_IDS['carga']
    eje_giro = ctrl_vars.AXIS_IDS['giro']
    error_messages = []
    initial_state = msg_app.StateMachine.EST_INITIAL
    # Paso 0 - Chequear condiciones iniciales - Todos los valores deben ser True par que empiece la rutina
    init_flags = [
        (ws_vars.MicroState.axis_flags[eje_carga]['estado'] != 'safe', 'Eje carga en safe'),      # Eje en safe
        (ws_vars.MicroState.axis_flags[eje_giro]['estado'] != 'safe', 'Eje husillo en safe'),     # Eje en safe
        (ws_vars.MicroState.axis_flags[eje_avance]['estado'] != 'safe', 'Eje avance en safe'),    # Eje en safe
        (ws_vars.MicroState.rem_i_states[1]['presion_normal'], 'Baja presión'),                 # Presión normal

        (ws_vars.MicroState.axis_flags[eje_avance]['maq_est_val'] == initial_state, 'Eje lineal apagado'),      # eje avance encendido
        (ws_vars.MicroState.rem_i_states[1]['acople_lubric_contraido'], 'Acople lubricante afuera'),            # acople_lubricante_contraido
        (ws_vars.MicroState.rem_i_states[0]['puntera_descarga_contraida'], 'Puntera descarga expandida'),       # puntera_descarga_contraida
        (ws_vars.MicroState.rem_i_states[0]['puntera_carga_contraida'], 'Puntera carga expandida'),             # puntera_carga_contraida
    ]

    for flag, error in init_flags:
        if flag == False:
            error_messages.append(error)

    return error_messages



# ********* condiciones iniciales - INDEX *********
def check_init_conditions_index():
    pos = round(ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['carga']]['pos_fil'], 0)
    eje_avance = ctrl_vars.AXIS_IDS['avance']
    eje_carga = ctrl_vars.AXIS_IDS['carga']
    eje_giro = ctrl_vars.AXIS_IDS['giro']
    error_messages = []
    eje_avance = ctrl_vars.AXIS_IDS['avance']
    init_flags = [
        (pos in ctrl_vars.LOAD_STEPS, 'Posición de plato errónea'),                                                                     # Plato alineado
        (ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['avance']]['cero_desconocido'] == False, 'Cero desconocido en eje lineal'),   # Eje lineal cerado
        (ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['carga']]['cero_desconocido'] == False, 'Cero desconocido en eje lineal'),    # Cabezal cerado
        
        (ws_vars.MicroState.axis_flags[eje_carga]['estado'] != 'safe', 'Eje carga en safe'),                                              # Eje en safe
        (ws_vars.MicroState.axis_flags[eje_giro]['estado'] != 'safe', 'Eje husillo en safe'),                                             # Eje en safe
        (ws_vars.MicroState.axis_flags[eje_avance]['estado'] != 'safe', 'Eje avance en safe'),                                            # Eje en safe
        (ws_vars.MicroState.rem_i_states[1]['presion_normal'], 'Baja presión'),                                                         # Presión normal

        (ws_vars.MicroState.rem_i_states[1]['clampeo_plato_expandido'], 'Plato no clampeado'),                                          # plato_clampeado
        (ws_vars.MicroState.rem_i_states[1]['acople_lubric_contraido'], 'Acople lubricante expandido'),                                 # acople_lubricante_contraido
        (ws_vars.MicroState.rem_i_states[0]['puntera_descarga_contraida'], 'Puntera descarga expandida'),                               # puntera_descarga_contraida
        (ws_vars.MicroState.rem_i_states[0]['puntera_carga_contraida'], 'Puntera carga expandida'),                                     # puntera_carga_contraida
        (round(ws_vars.MicroState.axis_measures[eje_avance]['pos_fil'], 0) == round(ctrl_vars.ROSCADO_CONSTANTES['posicion_de_inicio'], 0), 'Posición de eje avance erróneo'),   # Eje avance en posición de inicio
    ]
    for flag, error in init_flags:
        if flag == False:
            error_messages.append(error)

    return error_messages



# ********* condiciones iniciales - CARGA *********
def check_init_conditions_load():
    pos = round(ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['carga']]['pos_fil'], 0)
    eje_avance = ctrl_vars.AXIS_IDS['avance']
    eje_carga = ctrl_vars.AXIS_IDS['carga']
    eje_giro = ctrl_vars.AXIS_IDS['giro']
    error_messages = []
    init_flags = [
        (pos in ctrl_vars.LOAD_STEPS, 'Posición de plato errónea'),                                                                     # Plato alineado
        (ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['avance']]['cero_desconocido'] == False, 'Cero desconocido en eje lineal'),   # Eje lineal cerado
        (ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['carga']]['cero_desconocido'] == False, 'Cero desconocido en eje lineal'),    # Cabezal cerado

        (ws_vars.MicroState.rem_i_states[1]['presion_normal'], 'Baja presión'),                                                         # Presión normal
        (ws_vars.MicroState.axis_flags[eje_carga]['estado'] != 'safe', 'Eje carga en safe'),                                              # Eje en safe
        (ws_vars.MicroState.axis_flags[eje_giro]['estado'] != 'safe', 'Eje husillo en safe'),                                             # Eje en safe
        (ws_vars.MicroState.axis_flags[eje_avance]['estado'] != 'safe', 'Eje avance en safe'),                                            # Eje en safe

        (ws_vars.MicroState.rem_o_states[1]['encender_bomba_hidraulica'], 'Bomba hidráulica apagada'),              # hidráulica ON
        (ws_vars.MicroState.rem_i_states[1]['clampeo_plato_expandido'], 'Plato no clampeado'),                      # Plato clampeado
        (ws_vars.MicroState.rem_i_states[0]['vertical_carga_contraido'], 'Vertical de carga expandido'),            # vertical_carga_contraido
        (ws_vars.MicroState.rem_i_states[0]['puntera_carga_contraida'], 'Puntera carga expandida'),                 # puntera_carga_contraida
        (ws_vars.MicroState.rem_i_states[0]['brazo_cargador_expandido'], 'Brazo cargador cntraído'),                # brazo_cargador_expandido
        (ws_vars.MicroState.rem_i_states[0]['boquilla_carga_expandida'], 'Boquilla de carga contraída'),            # boquilla de carga  liberada - ws_vars.MicroState.rem_i_states[0]
        (ws_vars.MicroState.rem_i_states[1]['presencia_cupla_en_cargador'], 'Cupla en cargador no presente'),       # presencia_cupla_en_cargador
        (not ws_vars.MicroState.rem_i_states[1]['pieza_en_boquilla_carga'], 'Pieza en boquilla de carga presente')  # pieza no presente en boquilla de carga
    ]

    for flag, error in init_flags:
        if flag == False:
            error_messages.append(error)
    
    return error_messages



# ********* condiciones iniciales - DESCARGA *********
def check_init_conditions_unload():
    pos = round(ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['carga']]['pos_fil'], 0)
    eje_avance = ctrl_vars.AXIS_IDS['avance']
    eje_carga = ctrl_vars.AXIS_IDS['carga']
    eje_giro = ctrl_vars.AXIS_IDS['giro']
    error_messages = []
    init_flags = [
        (pos in ctrl_vars.LOAD_STEPS, 'Posición de plato errónea'),                                                                     # Plato alineado
        (ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['avance']]['cero_desconocido'] == False, 'Cero desconocido en eje lineal'),   # Eje lineal cerado
        (ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['carga']]['cero_desconocido'] == False, 'Cero desconocido en eje lineal'),    # Cabezal cerado

        (ws_vars.MicroState.rem_i_states[1]['presion_normal'], 'Baja presión'),                                                         # Presión normal
        (ws_vars.MicroState.axis_flags[eje_carga]['estado'] != 'safe', 'Eje carga en safe'),                                              # Eje en safe
        (ws_vars.MicroState.axis_flags[eje_giro]['estado'] != 'safe', 'Eje husillo en safe'),                                             # Eje en safe
        (ws_vars.MicroState.axis_flags[eje_avance]['estado'] != 'safe', 'Eje avance en safe'),                                            # Eje en safe

        (ws_vars.MicroState.rem_o_states[1]['encender_bomba_hidraulica'], 'Bomba hidráulica apagada'),                      # hidráulica ON
        (ws_vars.MicroState.rem_i_states[1]['clampeo_plato_expandido'], 'Plato no clampeado'),                              # Plato clampeado
        (ws_vars.MicroState.rem_i_states[0]['puntera_descarga_contraida'], 'Puntera descarga expandida'),                   # puntera_descarga_contraida
        (ws_vars.MicroState.rem_i_states[0]['brazo_descarga_expandido'], 'Brazo descargador contraído'),                    # brazo_descarga_expandido
        (ws_vars.MicroState.rem_i_states[0]['boquilla_descarga_expandida'], 'Boquilla descarga contraída'),                 # boquilla descarga liberada - boquilla_descarga_expandida
        (ws_vars.MicroState.rem_i_states[1]['cupla_por_tobogan_descarga'], 'Cupla presente en tobogán de descarga'),        # cupla no presente en tobogan_descarga
        (not ws_vars.MicroState.rem_i_states[1]['pieza_en_boquilla_descarga'], 'Cupla presente en boquilla de descarga'),   # cupla no presente en boquilla descarga
        (ws_vars.MicroState.rem_i_states[1]['horiz_pinza_desc_contraido'], 'Horizontal pinza de descarga expandida'),       # horiz_pinza_desc_contraido
        (ws_vars.MicroState.rem_i_states[1]['vert_pinza_desc_contraido'], 'Vertical pinza de descarga expandida'),          # vert_pinza_desc_contraido
        (ws_vars.MicroState.rem_i_states[0]['pinza_descargadora_abierta'], 'Pinza descargadora cerrada')                    # pinza_descargadora_abierta
    ]

    for flag, error in init_flags:
        if flag == False:
            error_messages.append(error)
    
    return error_messages



# ********* condiciones iniciales - ROSCADO *********
def check_init_conditions_tapping():
    pos = round(ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['carga']]['pos_fil'], 0)
    eje_avance = ctrl_vars.AXIS_IDS['avance']
    eje_carga = ctrl_vars.AXIS_IDS['carga']
    eje_giro = ctrl_vars.AXIS_IDS['giro']
    initial_state = msg_app.StateMachine.EST_INITIAL
    
    sync_flag = None
    sync_err_msg = None
    if ws_vars.MicroState.master_running == False or ws_vars.MicroState.iteration <= 1:
        sync_flag = ws_vars.MicroState.axis_flags[eje_avance]['sync_on'] == 0   # Si master no está corriendo o la iteración es <= 1 (todavía no empezó a roscar)
                                                                                # el sync tiene que estar apagado (sync_flag = 1)
        sync_err_msg = 'Sincronismo encendido'
    else:
        sync_flag = ws_vars.MicroState.axis_flags[eje_avance]['sync_on'] == 1
        sync_err_msg = 'Sincronismo apagado con master'
    error_messages = []

    init_flags = [
        (pos in ctrl_vars.LOAD_STEPS, 'Posición de plato errónea'),                                                                     # Plato alineado
        (ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['avance']]['cero_desconocido'] == False, 'Cero desconocido en eje lineal'),   # Eje lineal cerado
        (ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['carga']]['cero_desconocido'] == False, 'Cero desconocido en eje lineal'),    # Cabezal cerado

        (ws_vars.MicroState.rem_i_states[1]['presion_normal'], 'Baja presión'),                                                         # Presión normal
        (ws_vars.MicroState.axis_flags[eje_carga]['estado'] != 'safe', 'Eje carga en safe'),                                              # Eje en safe
        (ws_vars.MicroState.axis_flags[eje_giro]['estado'] != 'safe', 'Eje husillo en safe'),                                             # Eje en safe
        (ws_vars.MicroState.axis_flags[eje_avance]['estado'] != 'safe', 'Eje avance en safe'),                                            # Eje en safe

        (ws_vars.MicroState.rem_o_states[1]['encender_bomba_hidraulica'], 'Bomba hidráulica apagada'),                                  # hidráulica ON
        (ws_vars.MicroState.rem_i_states[1]['clampeo_plato_expandido'], 'Plato no clampeado'),                                          # Plato clampeado
        (ws_vars.MicroState.rem_i_states[1]['acople_lubric_contraido'], 'Acople lubricante afuera'),                                    # acople_lubricante_contraido
        (ws_vars.MicroState.axis_flags[eje_avance]['maq_est_val'] == initial_state, 'Eje de avance apagado'),                           # eje avance ON
        (ws_vars.MicroState.axis_flags[eje_carga]['drv_flags'] & msg_base.DrvFbkDataFlags.ENABLED == 0, 'Eje de carga encendido'),      # eje carga OFF
        (sync_flag, sync_err_msg),                                                                                                      # Sincronismo
        (round(ws_vars.MicroState.axis_measures[eje_avance]['pos_fil'], 0) == round(ctrl_vars.ROSCADO_CONSTANTES['posicion_de_inicio'], 0), 'Posición de eje de avance errónea')   # Eje avance en posición de inicio
    ]

    for flag, error in init_flags:
        if flag == False:
            error_messages.append(error)
    
    return error_messages


def get_running_routines():
    from apps.control.models import RoutineInfo
    routines = RoutineInfo.objects.all()
    running_routines = []
    for rtn in routines:
        if rtn.running == 1:
            running_routines.append(rtn.name)
    return running_routines


def check_routine_allowed(routine):
    running_rtns = get_running_routines()
    homing_name = ctrl_vars.ROUTINE_NAMES[ctrl_vars.ROUTINE_IDS['cerado']]
    cabezal_indexar = ctrl_vars.ROUTINE_NAMES[ctrl_vars.ROUTINE_IDS['cabezal_indexar']]
    roscado = ctrl_vars.ROUTINE_NAMES[ctrl_vars.ROUTINE_IDS['roscado']]
    routine_name = ctrl_vars.ROUTINE_NAMES[routine]

    if running_rtns:

        if homing_name in running_rtns:
            print('Cerado en proceso')
            return False

        if cabezal_indexar in running_rtns:
            print('indexado en proceso')
            return False
    
        if routine_name == homing_name or routine_name in running_rtns:
            print('Rutina en proceso')
            return False
    
        if routine_name == cabezal_indexar and roscado in running_rtns:
            print('Indexar prohibido: roscado en proceso')
            return False
    
    return True


def reset_routines_info():
    from apps.control.models import RoutineInfo
    rtns_info = RoutineInfo.objects.all()
    for rtn in rtns_info:
        rtn.running = 0
        rtn.save()

# -------------------------------------------------------------------------------------------- #
# -------------------------------- Update/Get States ----------------------------------------- #
# -------------------------------------------------------------------------------------------- #


def update_data_flags(micro_data):
    cmd_toggle_bit = 1 << 0
    cmd_received_bit = 1 << 1
    
    em_stop_bit = 1 << 0
    ctrl_ok_bit = 1 << 1
    running_bit = 1 << 2

    micro_flags = {
        'cmd_toggle':   not (ws_vars.MicroState.last_rx_data.data.flags & cmd_toggle_bit == micro_data.data.flags & cmd_toggle_bit),
        'cmd_received': (micro_data.data.flags & cmd_received_bit == cmd_received_bit),
        'em_stop':      micro_data.data.ctrl.flags & em_stop_bit == em_stop_bit,
        'ctrl_ok':      micro_data.data.ctrl.flags & ctrl_ok_bit == ctrl_ok_bit,
        'running':      micro_data.data.ctrl.flags & running_bit == running_bit
    }

    ws_vars.MicroState.micro_flags = micro_flags
    return micro_flags


def check_end_flags(flags_value):
    ok_bit                  = msg_app.AxisFlagsFin.FLGFIN_OK
    cancel_bit              = msg_app.AxisFlagsFin.FLGFIN_CANCELLED
    em_stop_bit             = msg_app.AxisFlagsFin.FLGFIN_EM_STOP
    drv_homing_err_bit      = msg_app.AxisFlagsFin.FLGFIN_DRV_HOMING_ERROR
    echo_timeout_bit        = msg_app.AxisFlagsFin.FLGFIN_ECHO_TIMEOUT
    pos_abs_disabled_bit    = msg_app.AxisFlagsFin.FLGFIN_POS_ABS_DISABLED
    unkown_zero_bit         = msg_app.AxisFlagsFin.FLGFIN_UNKNOWN_ZERO
    pos_fbk_err_bit         = msg_app.AxisFlagsFin.FLGFIN_POS_FEEDBACK_ERROR
    limit_vel_exceeded_bit  = msg_app.AxisFlagsFin.FLGFIN_LIMIT_VEL_EXCEEDED
    limit_pos_exceeded_bit  = msg_app.AxisFlagsFin.FLGFIN_LIMIT_POS_EXCEEDED
    limit_fza_exceeded_bit  = msg_app.AxisFlagsFin.FLGFIN_LIMIT_FZA_EXCEEDED
    yield_bit               = msg_app.AxisFlagsFin.FLGFIN_YIELD
    invalid_state_bit       = msg_app.AxisFlagsFin.FLGFIN_INVALID_STATE
    drv_not_enabled_bit     = msg_app.AxisFlagsFin.FLGFIN_DRV_NOT_ENABLED
    axis_disabled_bit       = msg_app.AxisFlagsFin.FLGFIN_AXIS_DISABLED

    end_states = []

    if flags_value & ok_bit == ok_bit:
        end_states = 'ok'
    else:
        if flags_value & cancel_bit == cancel_bit:
            end_states.append('cancel')
            ws_vars.MicroState.err_messages.append('Comando cancelado')
        if flags_value & em_stop_bit == em_stop_bit:
            end_states.append('em_stop')
            ws_vars.MicroState.err_messages.append('Parada de emergencia')
        if flags_value & drv_homing_err_bit == drv_homing_err_bit:
            end_states.append('homming_error')
            ws_vars.MicroState.err_messages.append('Error de cerado')
        if flags_value & echo_timeout_bit == echo_timeout_bit:
            end_states.append('echo_timeout')
            ws_vars.MicroState.err_messages.append('Eco tiemout')
        if flags_value & pos_abs_disabled_bit == pos_abs_disabled_bit:
            end_states.append('pos_abs_disabled')
            ws_vars.MicroState.err_messages.append('Posicion absuluta deshabilitada')
        if flags_value & unkown_zero_bit == unkown_zero_bit:
            end_states.append('unkown_zero')
            ws_vars.MicroState.err_messages.append('Cero desconocido')
        if flags_value & pos_fbk_err_bit == pos_fbk_err_bit:
            end_states.append('pos_fbk_err')
            ws_vars.MicroState.err_messages.append('Position feedback error')
        if flags_value & limit_vel_exceeded_bit == limit_vel_exceeded_bit:
            end_states.append('limit_vel_exceeded')
            ws_vars.MicroState.err_messages.append('Limite de velocidad exedido')
        if flags_value & limit_pos_exceeded_bit == limit_pos_exceeded_bit:
            end_states.append('limit_pos_exceeded')
            ws_vars.MicroState.err_messages.append('Limite de posicion exedido')
        if flags_value & limit_fza_exceeded_bit == limit_fza_exceeded_bit:
            end_states.append('limit_fza_exceeded')
            ws_vars.MicroState.err_messages.append('Limite de fuerza exedido')
        if flags_value & yield_bit == yield_bit:
            end_states.append('yield')
        if flags_value & invalid_state_bit == invalid_state_bit:
            end_states.append('invalid_state')
            ws_vars.MicroState.err_messages.append('Estado invalido')
        if flags_value & drv_not_enabled_bit == drv_not_enabled_bit:
            end_states.append('drv_not_enabled')
            ws_vars.MicroState.err_messages.append('Driver not enabled')
        if flags_value & axis_disabled_bit == axis_disabled_bit:
            end_states.append('axis_disabled')
            ws_vars.MicroState.err_messages.append('Axis disabled')
    
    return end_states


def update_axis_flags(micro_data, axis):
    flag = msg_app.AcdpAxisMovementsMovEjeDataFlagsBits.slave
    ws_vars.MicroState.axis_flags[axis]['slave']            = micro_data.data.ctrl.eje[axis].flags & flag == flag

    flag = msg_app.AcdpAxisMovementsMovEjeDataFlagsBits.sync_on
    ws_vars.MicroState.axis_flags[axis]['sync_on']          = micro_data.data.ctrl.eje[axis].flags & flag == flag
    
    flag = msg_app.AcdpAxisMovementsMovEjeDataFlagsBits.em_stop
    ws_vars.MicroState.axis_flags[axis]['em_stop']          = micro_data.data.ctrl.eje[axis].flags & flag == flag

    ws_vars.MicroState.axis_flags[axis]['maq_est_val']      = micro_data.data.ctrl.eje[axis].maq_est.estado
    ws_vars.MicroState.axis_flags[axis]['estado']           = msg_app.StateMachine.get_state(ws_vars.MicroState.axis_flags[axis]['maq_est_val'])

    flag = msg_base.DrvFbkDataFlags.UNKNOWN_ZERO
    ws_vars.MicroState.axis_flags[axis]['cero_desconocido'] = micro_data.data.ctrl.eje[axis].mov_pos.med_drv.drv_fbk.flags & flag  == flag

    flag = msg_base.DrvFbkDataFlags.HOME_SWITCH
    ws_vars.MicroState.axis_flags[axis]['home_switch']      = micro_data.data.ctrl.eje[axis].mov_pos.med_drv.drv_fbk.flags & flag == flag
    
    ws_vars.MicroState.axis_flags[axis]['drv_fbk_flags']    = micro_data.data.ctrl.eje[axis].mov_pos.med_drv.drv_fbk.flags

    ws_vars.MicroState.axis_flags[axis]['flags_fin']        = micro_data.data.ctrl.eje[axis].maq_est.flags_fin
    ws_vars.MicroState.axis_flags[axis]['fin']              = check_end_flags(ws_vars.MicroState.axis_flags[axis]['flags_fin'])
    ws_vars.MicroState.axis_flags[axis]['axis_id']          = axis

    ws_vars.MicroState.axis_flags[axis]['drv_flags']        = micro_data.data.ctrl.eje[axis].mov_pos.med_drv.drv_fbk.flags


def update_axis_data(micro_data):
    for i in range(ctrl_vars.AXIS_IDS['axis_amount']):
        update_axis_flags(micro_data, i)
        ws_vars.MicroState.axis_measures[i]['pos_fil'] = micro_data.data.ctrl.eje[i].mov_pos.med_drv.pos_fil
        ws_vars.MicroState.axis_measures[i]['vel_fil'] = micro_data.data.ctrl.eje[i].mov_pos.med_drv.vel_fil
        ws_vars.MicroState.axis_measures[i]['torque_fil'] = micro_data.data.ctrl.eje[i].mov_pos.med_drv.torque_fil
        ws_vars.MicroState.axis_measures[i]['pos_abs'] = micro_data.data.ctrl.eje[i].mov_pos.med_drv.drv_fbk.pos_abs
    
    if ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['carga']]['estado'] == 'initial' and ws_vars.MicroState.rem_i_states[1]['clampeo_plato_expandido']:
        time_diff = datetime.now() - ws_vars.MicroState.load_on_timer
        if time_diff.total_seconds() >= ctrl_vars.CABEZAL_ON_TIMEOFF:
            print('Cabezal timeout excedido')
            ws_vars.MicroState.err_messages.append('Tiempo de cabezal encendido con clampeo excedido')
            ws_vars.MicroState.turn_load_drv_off = True
    else:
        ws_vars.MicroState.load_on_timer = datetime.now()
    
    enable_flag = msg_base.DrvFbkDataFlags.ENABLED
    if ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['giro']]['drv_flags'] & enable_flag and \
        round(ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['giro']]['vel_fil'], 0) == 0:
        
        from apps.control.models import RoutineInfo
        roscado_info = RoutineInfo.objects.get(name='roscado')

        if roscado_info.running == 0 and ws_vars.MicroState.master_running == 0:
            time_diff = datetime.now() - ws_vars.MicroState.turn_on_timer
            if time_diff.total_seconds() >= ctrl_vars.GIRO_ON_TIMEOUT:
                ws_vars.MicroState.turn_turn_drv_off = True
    
    else:
        ws_vars.MicroState.turn_on_timer = datetime.now()


def update_rem_io_states(micro_data):
    g_1_i = {}
    g_2_i = {}
    g_1_o = {}
    g_2_o = {}
    ws_vars.MicroState.rem_i_states = []
    ws_vars.MicroState.rem_o_states = []
    ws_vars.MicroState.rem_i = []
    ws_vars.MicroState.rem_o = []
    for i in range(len(ctrl_vars.REM_DI_G1_STATES)):
        keys = (
            ctrl_vars.REM_DI_G1_ARR[i],
            ctrl_vars.REM_DI_G2_ARR[i],
            ctrl_vars.REM_DO_G1_ARR[i],
            ctrl_vars.REM_DO_G2_ARR[i]
            )
        flag = 1 << i
        if keys[0]:
            g_1_i[keys[0]] = (micro_data.data.ctrl.rem_io.di16[0] & flag == flag)
            ctrl_vars.REM_DI_G1_STATES[keys[0]] = g_1_i[keys[0]]
        if keys[1]:
            g_2_i[keys[1]] = (micro_data.data.ctrl.rem_io.di16[1] & flag == flag)
            ctrl_vars.REM_DI_G2_STATES[keys[1]] = g_2_i[keys[1]]
        if keys[2]:
            g_1_o[keys[2]] = (micro_data.data.ctrl.rem_io.do16[0] & flag == flag)
            ctrl_vars.REM_DO_G1_STATES[keys[2]] = g_1_o[keys[2]]
        if keys[3]:
            g_2_o[keys[3]] = (micro_data.data.ctrl.rem_io.do16[1] & flag == flag)
            ctrl_vars.REM_DO_G2_STATES[keys[3]] = g_2_o[keys[3]]
    states = {
        'i1': g_1_i,
        'i2': g_2_i,
        'o1': g_1_o,
        'o2': g_2_o
    }
    ws_vars.MicroState.rem_i_states.append(g_1_i)
    ws_vars.MicroState.rem_i_states.append(g_2_i)
    ws_vars.MicroState.rem_o_states.append(g_1_o)
    ws_vars.MicroState.rem_o_states.append(g_2_o)
    ws_vars.MicroState.rem_i.append(micro_data.data.ctrl.rem_io.di16[0])
    ws_vars.MicroState.rem_i.append(micro_data.data.ctrl.rem_io.di16[1])
    ws_vars.MicroState.rem_o.append(micro_data.data.ctrl.rem_io.do16[0])
    ws_vars.MicroState.rem_o.append(micro_data.data.ctrl.rem_io.do16[1])
    return states


def update_loc_io_states(micro_data):
    loc_in = {}
    loc_out = {}
    for i in range(len(ctrl_vars.LOC_DI_ARR)):
        flag = 1 << i
        key = ctrl_vars.LOC_DI_ARR[i]
        loc_in[key] = (micro_data.data.ctrl.loc_io.di16 & flag == flag)
        ctrl_vars.LOC_DI_STATES[key] = loc_in[key]
        ws_vars.MicroState.loc_i[key] = micro_data.data.ctrl.loc_io.di16 & flag
    
    for i in range(len(ctrl_vars.LOC_DO_ARR)):
        flag = 1 << i
        key = ctrl_vars.LOC_DO_ARR[i]
        loc_out[key] = (micro_data.data.ctrl.loc_io.do16 & flag == flag)
        ctrl_vars.LOC_DO_STATES[key] = loc_out[key]
        ws_vars.MicroState.loc_o[key] = micro_data.data.ctrl.loc_io.do16 & flag
    
    states = {
        'i': loc_in,
        'o': loc_out
    }
    ws_vars.MicroState.loc_i_states = loc_in
    ws_vars.MicroState.loc_o_states = loc_out
    # print(ws_vars.MicroState.loc_i_states)
    return states


def update_io_states(micro_data):
    update_rem_io_states(micro_data)
    update_loc_io_states(micro_data)


def update_graph():
    if ws_vars.MicroState.graph_flag == True:
        position_value = ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['avance']]['pos_fil']
        torque_value = ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['giro']]['torque_fil']
        ws_vars.MicroState.position_values.append(position_value)
        ws_vars.MicroState.torque_values.append(torque_value)


def update_states(micro_data):
    update_io_states(micro_data)
    update_data_flags(micro_data)
    update_axis_data(micro_data)
    update_graph()
    update_front_states()           # Should always be called at the end


def update_front_messages():
    now_time = datetime.now()
    timestamp = now_time.strftime("%m/%d/%y %H:%M:%S")
    if ws_vars.MicroState.log_messages:
        log_messages = []
        for msg in ws_vars.MicroState.log_messages:
            msg = timestamp + ' - ' + msg
            log_messages.append(msg)
        ws_vars.MicroState.log_messages = log_messages
    
    if ws_vars.MicroState.err_messages:
        time_diff = now_time - ws_vars.MicroState.last_err_time
        if ws_vars.MicroState.err_messages != ws_vars.MicroState.last_err_msg or time_diff.total_seconds() >= ws_vars.MicroState.err_msg_refresh_timer:
            ws_vars.MicroState.last_err_msg = ws_vars.MicroState.err_messages
            ws_vars.MicroState.last_err_time = now_time
            err_messages = []
            for msg in ws_vars.MicroState.err_messages:
                msg = timestamp + ' - ' + msg
                err_messages.append(msg)
            ws_vars.MicroState.err_messages = err_messages
        else:
            ws_vars.MicroState.err_messages = []


def get_front_states():
    limit_fwd_flag = msg_base.DrvFbkDataFlags.POSITIVE_OT
    home_sw_flag = msg_base.DrvFbkDataFlags.HOME_SWITCH
    update_front_messages()
    
    data = {
        # Measures
        'husillo_rpm': ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['giro']]['vel_fil'],
        'husillo_torque': ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['giro']]['torque_fil'],

        'cabezal_pos': ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['carga']]['pos_fil'],
        'cabezal_vel': ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['carga']]['vel_fil'],

        'avance_pos': ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['avance']]['pos_fil'],
        'avance_vel': ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['avance']]['vel_fil'],

        # Axis states
        'lineal_enable': ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['avance']]['estado'] == 'initial',
        'cabezal_enable': ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['carga']]['estado'] == 'initial',
        'husillo_enable': ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['giro']]['estado'] == 'initial',

        'lineal_cero_desconocido': ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['avance']]['cero_desconocido'],
        'cabezal_cero_desconocido': ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['carga']]['cero_desconocido'],

        'remote_inputs': ws_vars.MicroState.rem_i_states,
        'remote_outputs': ws_vars.MicroState.rem_o_states,

        'flags_fin_eje_carga': ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['carga']]['flags_fin'],
        'estado_eje_carga': ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['carga']]['estado'],

        'flags_fin_eje_avance': ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['avance']]['flags_fin'],
        'estado_eje_avance': ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['avance']]['estado'],

        'flags_fin_eje_giro': ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['giro']]['flags_fin'],
        'estado_eje_giro': ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['giro']]['estado'],

        'sync_on_avance': ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['avance']]['sync_on'],
        'slave_giro': ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['giro']]['slave'],

        'lineal_limite_forward': ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['avance']]['drv_fbk_flags'] & limit_fwd_flag == 0,
        'lineal_home_switch': ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['avance']]['drv_fbk_flags'] & home_sw_flag == home_sw_flag,
        'cabezal_home_switch': ws_vars.MicroState.axis_flags[ctrl_vars.AXIS_IDS['carga']]['drv_fbk_flags'] & home_sw_flag == home_sw_flag,

        # Routines
        'condiciones_init_carga_ok': len(check_init_conditions_load()) == 0,
        'condiciones_init_descarga_ok': len(check_init_conditions_unload()) == 0,
        'condiciones_init_indexar_ok': len(check_init_conditions_index()) == 0,
        'condiciones_init_roscado_ok': len(check_init_conditions_tapping()) == 0,
        'homing_on_going': ws_vars.MicroState.homing_ongoing,
        'end_master_routine': ws_vars.MicroState.end_master_routine,

        # 'graph': ws_vars.MicroState.graph_flag
        'graph': False,
        'graph_flag': ws_vars.MicroState.graph_flag,

        'posicion_de_inicio': ctrl_vars.ROSCADO_CONSTANTES['posicion_de_inicio'],

        # Messages
        'mensajes_log': ws_vars.MicroState.log_messages,
        'mensajes_error': ws_vars.MicroState.err_messages,
    }
    return data


def update_front_states():
    data = get_front_states()
    send_front_message(data)
    ws_vars.MicroState.log_messages = []
    ws_vars.MicroState.err_messages = []

################################################################################################
######################################## COMMANDS ##############################################
################################################################################################


# -------------------------------------------------------------------------------------------- #
# ------------------------------ Set remote/local outputs ------------------------------------ #
# -------------------------------------------------------------------------------------------- #

def set_rem_do(command, key, group, bool_value):
    msg_id = ws_vars.MicroState.last_rx_header.get_msg_id() + 1
    ws_vars.MicroState.msg_id = msg_id

    mask = None
    out_value = bool_value
    
    if group == 0:
        bit = 0x0000 + 1 << ctrl_vars.REM_DO_G1_BITS[key]
    elif group == 1:
        bit = 0x0000 + 1 << ctrl_vars.REM_DO_G2_BITS[key]
    mask = bit

    if bool_value:
        out_value = bit
    else:
        out_value = 0
    return build_msg(command, msg_id=msg_id, mask=mask, out_value=out_value, group=group)


def toggle_rem_do(command, keys, group):
    msg_id = ws_vars.MicroState.last_rx_header.get_msg_id() + 1
    ws_vars.MicroState.msg_id = msg_id
    print('*********')
    mask = None
    out_value = None
    
    if type(keys) == type([]):
        key_1 = keys[0]
        key_2 = keys[1]
        print(key_1, key_2)

        if group == 0:
            bit_1 = 0x0000 + 1 << ctrl_vars.REM_DO_G1_BITS[key_1]
            bit_2 = 0x0000 + 1 << ctrl_vars.REM_DO_G1_BITS[key_2]
        elif group == 1:
            bit_1 = 0x0000 + 1 << ctrl_vars.REM_DO_G2_BITS[key_1]
            bit_2 = 0x0000 + 1 << ctrl_vars.REM_DO_G2_BITS[key_2]

        mask = bit_1 + bit_2
        state_1 = ws_vars.MicroState.rem_o_states[group][key_1]
        state_2 = ws_vars.MicroState.rem_o_states[group][key_2]
        print(bit_1)
        print(bit_2)
        if not state_1:
            out_value = bit_1
        elif not state_2:
            out_value = bit_2
    else:
        if group == 0:
            bit = 0x0000 + 1 << ctrl_vars.REM_DO_G1_BITS[keys]
        elif group == 1:
            bit = 0x0000 + 1 << ctrl_vars.REM_DO_G2_BITS[keys]
        mask = bit
        state = ws_vars.MicroState.rem_o_states[group][keys]
        if not state:
            out_value = bit
        else:
            out_value = 0
    return build_msg(command, msg_id=msg_id, mask=mask, out_value=out_value, group=group)


def set_loc_do(command, out_name, out_value):
    bit = None
    msg_id = ws_vars.MicroState.last_rx_header.get_msg_id() + 1
    ws_vars.MicroState.msg_id = msg_id
    bit = ctrl_vars.LOC_DO_BITS[out_name]
    mask = bit
    if ctrl_vars.LOC_DI_STATES[out_name]:
        out_value = 0
    else:
        out_value = bit
    return build_msg(Commands.loc_do_set, msg_id=msg_id, out_value=out_value, mask=mask)


# -------------------------------------------------------------------------------------------- #
# -------------------------------------- General --------------------------------------------- #
# -------------------------------------------------------------------------------------------- #


def sync_on(paso):
    msg_id = ws_vars.MicroState.last_rx_header.get_msg_id() + 1
    ws_vars.MicroState.msg_id = msg_id
    header = build_msg(Commands.sync_on, msg_id = msg_id, paso=paso)
    send_message(header)


def stop():
    msg_id = ws_vars.MicroState.last_rx_header.get_msg_id() + 1
    ws_vars.MicroState.msg_id = msg_id
    header = build_msg(Commands.stop, msg_id = msg_id)
    send_message(header)


def get_message_id():
    return ws_vars.MicroState.msg_id + 1