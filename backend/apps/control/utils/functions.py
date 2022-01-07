from apps.service.acdp.handlers import build_msg
from apps.service.api.variables import COMMANDS
from apps.control.utils import variables as var

def init_rem_io():
    for i in range(len(var.REM_DI_G1_ARR)):
        key = var.REM_DI_G1_ARR[i]
        if key: var.REM_DI_G1_DICT[key] = None
        key = var.REM_DI_G2_ARR[i]
        if key: var.REM_DI_G2_DICT[key] = None
        key = var.REM_DO_G1_ARR[i]
        if key: var.REM_DO_G1_DICT[key] = None
        key = var.REM_DO_G2_ARR[i]
        if key: var.REM_DO_G2_DICT[key] = None


def update_rem_io_states(micro_data):
    states = {}
    g_1_i = {}
    g_2_i = {}
    g_1_o = {}
    g_2_o = {}
    for i in range(len(var.REM_DI_G1_DICT)):
        keys = (
            var.REM_DI_G1_ARR[i],
            var.REM_DI_G2_ARR[i],
            var.REM_DO_G1_ARR[i],
            var.REM_DO_G2_ARR[i]
            )
        flag = 1 << i
        if keys[0]:
            g_1_i[keys[0]] = (micro_data.data.ctrl.rem_io.di16[0] & flag == flag)
            var.REM_DI_G1_DICT[keys[0]] = g_1_i[keys[0]]
        if keys[1]:
            g_2_i[keys[1]] = (micro_data.data.ctrl.rem_io.di16[1] & flag == flag)
            var.REM_DI_G2_DICT[keys[1]] = g_2_i[keys[1]]
        if keys[2]:
            g_1_o[keys[2]] = (micro_data.data.ctrl.rem_io.do16[0] & flag == flag)
            var.REM_DO_G1_DICT[keys[2]] = g_1_o[keys[2]]
        if keys[3]:
            g_2_o[keys[3]] = (micro_data.data.ctrl.rem_io.do16[1] & flag == flag)
            var.REM_DO_G2_DICT[keys[3]] = g_2_o[keys[3]]
    states['i1'] = g_1_i
    states['i2'] = g_2_i
    states['o1'] = g_1_o
    states['o2'] = g_2_o

    return states