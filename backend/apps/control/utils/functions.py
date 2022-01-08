from apps.service.acdp.handlers import build_msg
from apps.service.api.variables import Commands, COMMANDS
from apps.service.acdp import messages_app as msg_app
from apps.control.utils import variables as ctrl_vars
from apps.ws.utils.handlers import send_message
from apps.ws.utils.functions import get_ch_info
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


################################################################################################
######################################## COMMANDS ##############################################
################################################################################################


# -------------------------------------------------------------------------------------------- #
# ------------------------------ Set remote/local outputs ------------------------------------ #
# -------------------------------------------------------------------------------------------- #


def set_rem_do(command, keys, group):
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