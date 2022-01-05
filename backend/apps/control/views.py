from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import apps.service.acdp.handlers as service_handlers
from apps.service.api.variables import Commands
from apps.ws.utils.handlers import send_message
from apps.ws.utils.functions import get_ch_info
from apps.ws.models import ChannelInfo

# Create your views here.

@csrf_exempt
def manual(request):
    print(request.POST)
    ch_info = get_ch_info(ChannelInfo, 'micro')
    header = service_handlers.build_header(code=Commands.open_connection[0])
    if ch_info:
        send_message(header, ch_info)
    return JsonResponse({'resp': 'ok'})