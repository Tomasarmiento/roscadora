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

# Create your views here.

@csrf_exempt
def manual(request):
    post_req = request.POST
    ch_info = get_ch_info(ChannelInfo, 'micro')
    req_data = []
    params = {}
    MicroState.msg_id += 1
    msg_id = MicroState.msg_id
    
    for item in post_req.items():   # Item is in (key, value) format
        req_data.append(item)

    command = int(req_data[0][1])
    for item in req_data[1:]:
        params[item[0]] = float(item[1])

    header, data = service_handlers.build_msg(command, params=params, msg_id=msg_id)
    # msg = header.pacself() + data.pacself()
    if ch_info:
        print(ch_info)
        send_message(header, ch_info, data)
    return JsonResponse({'resp': 'ok'})