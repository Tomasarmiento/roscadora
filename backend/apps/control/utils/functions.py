import threading
import random, time
from datetime import datetime
from apps.service.acdp.handlers import build_msg
from apps.service.api.variables import Commands, COMMANDS
from apps.service.acdp import messages_app as msg_app
from apps.service.acdp import messages_base as msg_base

from apps.control.utils import variables as ctrl_vars

from apps.ws.utils.handlers import send_message
from apps.ws.utils.functions import send_front_message
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


def init_routine_info(routine_model):
    routines = routine_model.objects.all()
    rtn_names = []
    for routine in routines:
        rtn_names.append(routine.name)
    for rtn_name in ctrl_vars.ROUTINE_NAMES:
        if rtn_name not in rtn_names:
            routine_model.objects.create(name=rtn_name, running=0)


def init_comands_ref_rates():
    for key, value in ctrl_vars.COMMAND_DEFAULT_VALUES.items():
        ctrl_vars.COMMAND_REF_RATES[key] = value

# -------------------------------------------------------------------------------------------- #
# --------------------------------------- Routines ------------------------------------------- #
# -------------------------------------------------------------------------------------------- #


def get_running_routines(routine_model):
    routines = routine_model.objects.all()
    running_routines = []
    for rtn in routines:
        if rtn.running == 1:
            running_routines.append(rtn.name)
    return running_routines


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
        if flags_value & em_stop_bit == em_stop_bit:
            end_states.append('em_stop')
        if flags_value & drv_homing_err_bit == drv_homing_err_bit:
            end_states.append('homming_error')
        if flags_value & echo_timeout_bit == echo_timeout_bit:
            end_states.append('echo_timeout')
        if flags_value & pos_abs_disabled_bit == pos_abs_disabled_bit:
            end_states.append('pos_abs_disabled')
        if flags_value & unkown_zero_bit == unkown_zero_bit:
            end_states.append('unkown_zero')
        if flags_value & pos_fbk_err_bit == pos_fbk_err_bit:
            end_states.append('pos_fbk_err')
        if flags_value & limit_vel_exceeded_bit == limit_vel_exceeded_bit:
            end_states.append('limit_vel_exceeded')
        if flags_value & limit_pos_exceeded_bit == limit_pos_exceeded_bit:
            end_states.append('limit_pos_exceeded')
        if flags_value & limit_fza_exceeded_bit == limit_fza_exceeded_bit:
            end_states.append('limit_fza_exceeded')
        if flags_value & yield_bit == yield_bit:
            end_states.append('yield')
        if flags_value & invalid_state_bit == invalid_state_bit:
            end_states.append('invalid_state')
        if flags_value & drv_not_enabled_bit == drv_not_enabled_bit:
            end_states.append('drv_not_enabled')
        if flags_value & axis_disabled_bit == axis_disabled_bit:
            end_states.append('axis_disabled')
    
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
    
    # if axis == ctrl_vars.AXIS_IDS['carga']:
        # print(flag)
        # print(micro_data.data.ctrl.eje[axis].mov_pos.med_drv.drv_fbk.flags)
        # print(ws_vars.MicroState.axis_flags[axis]['homming_ended_ok'])
    
    ws_vars.MicroState.axis_flags[axis]['flags_fin']        = micro_data.data.ctrl.eje[axis].maq_est.flags_fin
    ws_vars.MicroState.axis_flags[axis]['fin']              = check_end_flags(ws_vars.MicroState.axis_flags[axis]['flags_fin'])
    ws_vars.MicroState.axis_flags[axis]['axis_id']          = axis


def update_axis_data(micro_data):
    for i in range(ctrl_vars.AXIS_IDS['axis_amount']):
        update_axis_flags(micro_data, i)
        ws_vars.MicroState.axis_measures[i]['pos_fil'] = micro_data.data.ctrl.eje[i].mov_pos.med_drv.pos_fil
        ws_vars.MicroState.axis_measures[i]['vel_fil'] = micro_data.data.ctrl.eje[i].mov_pos.med_drv.vel_fil
        ws_vars.MicroState.axis_measures[i]['torque_fil'] = micro_data.data.ctrl.eje[i].mov_pos.med_drv.torque_fil
        ws_vars.MicroState.axis_measures[i]['pos_abs'] = micro_data.data.ctrl.eje[i].mov_pos.med_drv.drv_fbk.pos_abs

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
    
    for i in range(len(ctrl_vars.LOC_DO_ARR)):
        flag = 1 << i
        key = ctrl_vars.LOC_DO_ARR[i]
        loc_out[key] = (micro_data.data.ctrl.loc_io.do16 & flag == flag)
        ctrl_vars.LOC_DO_STATES[key] = loc_out[key]
    
    states = {
        'i': loc_in,
        'o': loc_out
    }
    ws_vars.MicroState.loc_i_states = loc_in
    ws_vars.MicroState.loc_o_states = loc_out
    return states


def update_io_states(micro_data):
    update_rem_io_states(micro_data)
    update_loc_io_states(micro_data)


def update_states(micro_data):
    update_io_states(micro_data)
    update_data_flags(micro_data)
    update_axis_data(micro_data)
    update_front_states()


def get_front_states():
    data = {
        'husillo_rpm': ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['giro']]['vel_fil'],
        'husillo_torque': ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['giro']]['torque_fil'],

        'cabezal_pos': ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['carga']]['pos_fil'],
        'cabezal_vel': ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['carga']]['vel_fil'],

        'avance_pos': ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['avance']]['pos_fil'],
        'avance_vel': ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['avance']]['vel_fil']
    }
    return data


def update_front_states():
    data = get_front_states()
    send_front_message(data)

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

    mask = None
    out_value = None
    
    if type(keys) == type([]):
        key_1 = keys[0]
        key_2 = keys[1]

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
    send_message(header.pacself())


def stop():
    msg_id = ws_vars.MicroState.last_rx_header.get_msg_id() + 1
    ws_vars.MicroState.msg_id = msg_id
    header = build_msg(Commands.stop, msg_id = msg_id)
    send_message(header.pacself())