import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import apps.service.acdp.handlers as service_handlers
from apps.service.acdp.messages_app import AcdpAxisMovementEnums

from apps.service.api.variables import Commands
from apps.ws.utils.handlers import send_message
from apps.ws.utils.functions import get_ch_info
from apps.ws.utils.variables import MicroState
from apps.ws.models import ChannelInfo

from apps.control.utils.variables import COMMAND_DEFAULT_VALUES
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
                ref_rate = COMMAND_DEFAULT_VALUES['vel_eje_avance']
        elif axis == AcdpAxisMovementEnums.ID_X_EJE_CARGA:
            if 'ref_rate' in params.keys():
                ref_rate = params['ref_rate']
            else:
                ref_rate = COMMAND_DEFAULT_VALUES['vel_eje_carga']
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
    
    return JsonResponse({'resp': 'ok'})


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
            header, data = ctrl_func.set_rem_do(command, keys, 0)

        elif 'vertical' in name:
            keys = 'expandir_vertical_carga'
            header, data = ctrl_func.set_rem_do(command, keys, 0)

        elif name == 'BoquillaCarga':
            keys = 'contraer_boquilla_carga'
            header, data = ctrl_func.set_rem_do(command, keys, 0)

        elif 'giro' in name:
            keys = ['contraer_brazo_cargador', 'expandir_brazo_cargador']
            header, data = ctrl_func.set_rem_do(command, keys, 0)
    
    elif menu == 'descarga':
        if name == 'horizontalDesc':
            keys = ['contraer_puntera_descarga', 'expandir_puntera_descarga']
            header, data = ctrl_func.set_rem_do(command, keys, 0)
            
        elif name == 'giroDesc':
            keys = ['contraer_brazo_descargador', 'expandir_brazo_descargador']
            header, data = ctrl_func.set_rem_do(command, keys, 0)

        elif name == 'horizontalGr':
            keys = 'expandir_horiz_pinza_desc'
            header, data = ctrl_func.set_rem_do(command, keys, 1)

        elif name == 'verticalGr':          # REVISAR
            print('EXPANDIR VERT G')
            keys = 'expandir_vert_pinza_desc'
            header, data = ctrl_func.set_rem_do(command, keys, 1)

        elif name == 'BoquillaDesc':
            keys = 'contraer_boquilla_descarga'
            header, data = ctrl_func.set_rem_do(command, keys, 0)

        elif name == 'gripperDesc':
            keys = ['cerrar_pinza_descargadora', 'abrir_pinza_descargadora']
            header, data = ctrl_func.set_rem_do(command, keys, 0)
    
    elif menu == 'cabezal':
        if name == 'clampeo':
            keys = ['contraer_clampeo_plato', 'expandir_clampeo_plato']
            header, data = ctrl_func.set_rem_do(command, keys, 1)

        elif name == 'presion':
            keys = 'presurizar'
            header, data = ctrl_func.set_rem_do(command, keys, 1)

        elif name == 'boquilla1':
            keys = ['cerrar_boquilla_1', 'abrir_boquilla_1']
            header, data = ctrl_func.set_rem_do(command, keys, 1)

        elif name == 'boquilla2':
            keys = ['cerrar_boquilla_2', 'abrir_boquilla_2']
            header, data = ctrl_func.set_rem_do(command, keys, 1)

        elif name == 'boquilla3':
            keys = ['cerrar_boquilla_3', 'abrir_boquilla_3']
            header, data = ctrl_func.set_rem_do(command, keys, 1)

        elif name == 'acoplaSol':
            keys = 'expandir_acople_lubric'
            header, data = ctrl_func.set_rem_do(command, keys, 1)

        elif name == 'bombaSol':
            keys = 'encender_bomba_soluble'
            header, data = ctrl_func.set_rem_do(command, keys, 1)
        
        elif name == 'bombaHidr':
            keys = 'encender_bomba_hidraulica'
            header, data = ctrl_func.set_rem_do(command, keys, 1)
    
    if ch_info:
        print(header.get_values(), data.get_values())
        send_message(header, ch_info, data)
    return JsonResponse({'resp': 'ok'})


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
    
    return JsonResponse({'resp': 'ok'})