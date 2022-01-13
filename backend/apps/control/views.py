import json
import time

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import apps.service.acdp.handlers as service_handlers
from apps.service.acdp.messages_app import AcdpAxisMovementEnums, StateMachine

from apps.service.api.variables import Commands
from apps.ws.utils.handlers import send_message
from apps.ws.utils.functions import get_ch_info
from apps.ws.utils.variables import MicroState
from apps.ws.models import ChannelInfo

from apps.control.utils.variables import COMMAND_DEFAULT_VALUES
from apps.control.utils.routines import RoutineHandler
from apps.control.utils import variables as ctrl_vars
from apps.control.utils import functions as ctrl_func


@csrf_exempt
def manual_lineal(request):
    post_req = request.POST
    ch_info = get_ch_info(ChannelInfo, 'micro')
    req_data = []
    params = {}
    MicroState.msg_id += 1
    msg_id = MicroState.msg_id
    
    for item in post_req.items():   # Item is in (key, value) format
        req_data.append(item)

    command = int(req_data[0][1])
    axis = int(req_data[1][1])
    ref_rate = None
    print(params)
    if command != Commands.stop:
        for item in req_data[2:]:
            key = item[0]
            value = item[1]
            if key != 'abs':
                params[key] = float(value)
            else:
                params[key] = bool(value)
        
        if axis == AcdpAxisMovementEnums.ID_X_EJE_AVANCE:
            if 'ref_rate' in params.keys():
                ref_rate = params['ref_rate']
            else:
                ref_rate = COMMAND_DEFAULT_VALUES['vel_avance']
        elif axis == AcdpAxisMovementEnums.ID_X_EJE_CARGA:
            if 'ref_rate' in params.keys():
                ref_rate = params['ref_rate']
            else:
                ref_rate = COMMAND_DEFAULT_VALUES['vel_carga']
        if ref_rate:
            params['ref_rate'] = ref_rate
            if not params['abs']:
                pass
        
        header, data = service_handlers.build_msg(command, params=params, msg_id=msg_id, eje=axis)
    else:
        header = service_handlers.build_msg(command, msg_id=msg_id, eje=axis)
        data = None
    print(command, axis, params)

    if ch_info:
        send_message(header, ch_info, data)
    
    return JsonResponse({})


@csrf_exempt
def manual_pneumatic(request):
    post_req = request.POST
    ch_info = get_ch_info(ChannelInfo, 'micro')
    req_data = []
    MicroState.msg_id += 1
    msg_id = MicroState.msg_id
    
    for item in post_req.items():   # Item is in (key, value) format
        req_data.append(item)

    command = int(req_data[0][1])
    menu = req_data[1][1]
    name = req_data[2][1]
    if menu == 'carga':
        if 'horizontal' in name:
            keys = ['contraer_puntera_carga', 'expandir_puntera_carga']
            header, data = ctrl_func.toggle_rem_do(command, keys, 0)

        elif 'vertical' in name:
            keys = 'expandir_vertical_carga'
            header, data = ctrl_func.toggle_rem_do(command, keys, 0)

        elif name == 'BoquillaCarga':
            keys = 'contraer_boquilla_carga'
            header, data = ctrl_func.toggle_rem_do(command, keys, 0)

        elif 'giro' in name:
            keys = ['contraer_brazo_cargador', 'expandir_brazo_cargador']
            header, data = ctrl_func.toggle_rem_do(command, keys, 0)
    
    elif menu == 'descarga':
        if name == 'horizontalDesc':
            keys = ['contraer_puntera_descarga', 'expandir_puntera_descarga']
            header, data = ctrl_func.toggle_rem_do(command, keys, 0)
            
        elif name == 'giroDesc':
            keys = ['contraer_brazo_descargador', 'expandir_brazo_descargador']
            header, data = ctrl_func.toggle_rem_do(command, keys, 0)

        elif name == 'horizontalGr':
            keys = 'expandir_horiz_pinza_desc'
            header, data = ctrl_func.toggle_rem_do(command, keys, 1)

        elif name == 'verticalGr':
            keys = 'expandir_vert_pinza_desc'
            header, data = ctrl_func.toggle_rem_do(command, keys, 1)

        elif name == 'BoquillaDesc':
            keys = 'contraer_boquilla_descarga'
            header, data = ctrl_func.toggle_rem_do(command, keys, 0)

        elif name == 'gripperDesc':
            keys = ['cerrar_pinza_descargadora', 'abrir_pinza_descargadora']
            header, data = ctrl_func.toggle_rem_do(command, keys, 0)
    
    elif menu == 'cabezal':
        if name == 'clampeo':
            keys = ['contraer_clampeo_plato', 'expandir_clampeo_plato']
            header, data = ctrl_func.toggle_rem_do(command, keys, 1)

        elif name == 'presion':
            keys = 'presurizar'
            header, data = ctrl_func.toggle_rem_do(command, keys, 1)

        elif name == 'boquilla1':
            keys = ['cerrar_boquilla_1', 'abrir_boquilla_1']
            header, data = ctrl_func.toggle_rem_do(command, keys, 1)

        elif name == 'boquilla2':
            keys = ['cerrar_boquilla_2', 'abrir_boquilla_2']
            header, data = ctrl_func.toggle_rem_do(command, keys, 1)

        elif name == 'boquilla3':
            keys = ['cerrar_boquilla_3', 'abrir_boquilla_3']
            header, data = ctrl_func.toggle_rem_do(command, keys, 1)

        elif name == 'acoplaSol':
            keys = 'expandir_acople_lubric'
            header, data = ctrl_func.toggle_rem_do(command, keys, 1)

        elif name == 'bombaSol':
            keys = 'encender_bomba_soluble'
            header, data = ctrl_func.toggle_rem_do(command, keys, 1)
        
        elif name == 'bombaHidr':
            keys = 'encender_bomba_hidraulica'
            header, data = ctrl_func.toggle_rem_do(command, keys, 1)
    
    if ch_info:
        print(header.get_values(), data.get_values())
        send_message(header, ch_info, data)
    return JsonResponse({})


@csrf_exempt
def stop_axis(request):
    post_req = request.POST
    ch_info = get_ch_info(ChannelInfo, 'micro')
    req_data = []
    MicroState.msg_id += 1
    msg_id = MicroState.msg_id
    
    for item in post_req.items():   # Item is in (key, value) format
        req_data.append(item)

    command = int(req_data[0][1])
    axis = int(req_data[1][1])
    header = service_handlers.build_msg(command, msg_id=msg_id, eje=axis)
    print(command, axis)

    if ch_info:
        send_message(header, ch_info)
    
    return JsonResponse({})


@csrf_exempt
def stop_all(request):
    print('stop all')
    return JsonResponse({})


@csrf_exempt
def start_routine(request):
    command = Commands.drv_set_zero_abs
    msg_id = MicroState.last_rx_header.get_msg_id() + 1
    MicroState.msg_id = msg_id
    header, data = service_handlers.build_msg(command, msg_id=msg_id, zero=-7.2, eje=ctrl_vars.AXIS_IDS['carga'])
    ch_info = ChannelInfo.objects.get(source='micro')
    if ch_info:
        send_message(header, ch_info, data)
    return JsonResponse({})

@csrf_exempt
def semiauto(request):
    post_req = request.POST
    routine = int(post_req['routine'])
    RoutineHandler(routine).start()
    return JsonResponse({})


@csrf_exempt
def enable_axis(request):
    post_req = request.POST
    axis = int(post_req['eje'])
    cmd = int(post_req['command'])
    print(cmd, axis)
    msg_id = MicroState.last_rx_header.get_msg_id() + 1
    header = service_handlers.build_msg(cmd, msg_id=msg_id, eje=axis)
    ch_info = ChannelInfo.objects.get(source='micro')
    if ch_info:
        send_message(header, ch_info)
    return JsonResponse({})


@csrf_exempt
def sync_axis(request):
    post_req = request.POST
    msg_id = MicroState.last_rx_header.get_msg_id() + 1
    cmd = int(post_req['command'])
    ch_info = ChannelInfo.objects.get(source='micro')
    paso = None
    data = None
    header = None
    if 'paso' in post_req.keys() and cmd == Commands.sync_on:
        paso = float(post_req['paso'])
        header, data = service_handlers.build_msg(cmd, msg_id=msg_id, paso=paso, eje=ctrl_vars.AXIS_IDS['avance'])
    elif cmd == Commands.sync_off:
        header = service_handlers.build_msg(cmd, msg_id=msg_id, eje=ctrl_vars.AXIS_IDS['avance'])
    if header:
        if ch_info:
            send_message(header, ch_info, data)
    return JsonResponse({})