import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import apps.service.acdp.handlers as service_handlers
from apps.service.api.variables import Commands
from apps.ws.utils.handlers import send_message
from apps.ws.utils.functions import get_ch_info
from apps.ws.utils.variables import MicroState
from apps.ws.models import ChannelInfo

from apps.control.utils.variables import COMMAND_DEFAULT_VALUES
from apps.service.acdp.messages_app import AcdpAxisMovementEnums


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
    if command != Commands.stop[0]:
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