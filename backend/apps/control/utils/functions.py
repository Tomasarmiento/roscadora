from apps.service.acdp.handlers import build_msg
from apps.service.api.variables import Commands, COMMANDS
from apps.control.utils import variables as ctrl_vars
from apps.ws.utils.handlers import send_message
from apps.ws.utils import variables as ws_vars
from apps.service.acdp import messages_app as msg_app


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


def update_rem_io_states(micro_data):
    g_1_i = {}
    g_2_i = {}
    g_1_o = {}
    g_2_o = {}
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
    return states


def update_io_states(micro_data):
    update_rem_io_states(micro_data)
    update_loc_io_states(micro_data)


def set_rem_do(out_name, out_id, out_value):
    bit = None
    msg_id = ws_vars.MicroState.last_rx_header.get_msg_id() + 1
    ws_vars.MicroState.msg_id = msg_id
    bit = ctrl_vars.REM_DO_G2_BITS[out_name]
    header, data = build_msg(Commands.rem_do_set, bit=bit, msg_id=msg_id, out_value=out_value)
    msg = header.pacself() + data.pacself()
    send_message(msg)


def set_loc_do(out_name, out_id, out_value):
    bit = None
    msg_id = ws_vars.MicroState.last_rx_header.get_msg_id() + 1
    ws_vars.MicroState.msg_id = msg_id
    if out_id > 16: bit = ctrl_vars.REM_DO_G2_BITS[out_name]
    else:   bit = ctrl_vars.REM_DO_G1_BITS[out_name]
    header, data = build_msg(Commands.rem_do_set, bit=bit, msg_id=msg_id, out_value=out_value)
    msg = header.pacself() + data.pacself()
    send_message(msg)


def sync_on(paso):
    msg_id = ws_vars.MicroState.last_rx_header.get_msg_id() + 1
    ws_vars.MicroState.msg_id = msg_id
    header = build_msg(Commands.sync_on[0], msg_id = msg_id, paso=paso)
    send_message(header.pacself())


def stop():
    msg_id = ws_vars.MicroState.last_rx_header.get_msg_id() + 1
    ws_vars.MicroState.msg_id = msg_id
    header = build_msg(Commands.stop[0], msg_id = msg_id)
    send_message(header.pacself())