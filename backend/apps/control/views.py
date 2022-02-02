import json
import time

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import apps.service.acdp.handlers as service_handlers
from apps.service.acdp.messages_app import AcdpAxisMovementEnums, StateMachine
from apps.service.acdp.messages_base import AcdpMsgCmd

from apps.service.api.variables import Commands
from apps.ws.utils.handlers import send_message
from apps.ws.utils.functions import get_ch_info
from apps.ws.utils.variables import MicroState
from apps.ws.models import ChannelInfo

from apps.control.utils.variables import COMMAND_DEFAULT_VALUES
from apps.control.utils.routines import RoutineHandler
from apps.control.utils import variables as ctrl_vars
from apps.control.utils import functions as ctrl_func
from apps.control.models import RoutineInfo


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
    ch_info = get_ch_info(ChannelInfo, 'micro')
    msg_id = MicroState.msg_id
    command = AcdpMsgCmd.CD_STOP_ALL
    header = service_handlers.build_msg(command, msg_id=msg_id)
    if ch_info:
        send_message(header, ch_info)
    if MicroState.routine_ongoing == True:
        MicroState.routine_stopped = True
    MicroState.master_stop = True
    return JsonResponse({})


@csrf_exempt
def semiauto(request):
    post_req = request.POST
    routine = int(post_req['routine'])

    if ctrl_func.check_routine_allowed(RoutineInfo, routine):
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


@method_decorator(csrf_exempt, name='dispatch')
class StartRoutine(View):

    def get(self, request):
        print('GET req auto')
        return JsonResponse({})
    
    def post(self, request):
        if MicroState.master_running == True:
            print('Master ya está ejecutándose')
        
        else:
            MicroState.master_running = True
            MicroState.master_stop = False
            MicroState.iteration = 0
            roscado_id = ctrl_vars.ROUTINE_IDS['roscado']
            carga_id = ctrl_vars.ROUTINE_IDS['carga']
            descarga_id = ctrl_vars.ROUTINE_IDS['descarga']
            indexar_id = ctrl_vars.ROUTINE_IDS['cabezal_indexar']

            while MicroState.master_stop == False:
                running_ids = self.get_running_routines()
                print('\nRUNNING RTNS', running_ids)
                if carga_id not in running_ids:
                    print('RUTINA CARGA')
                    RoutineHandler(carga_id).start()

                    while carga_id not in running_ids:
                        time.sleep(0.2)
                        running_ids = self.get_running_routines()
                
                if MicroState.iteration >= 1:
                    if roscado_id not in running_ids:
                        print('RUTINA ROSCADO')
                        RoutineHandler(roscado_id).start()
                    
                    while roscado_id not in running_ids:
                        time.sleep(0.2)
                        running_ids = self.get_running_routines()
                
                if MicroState.iteration >= 2:
                    if descarga_id not in running_ids:
                        print('RUTINA DESCARGA')
                        RoutineHandler(descarga_id).start()
                    while descarga_id not in running_ids:
                        time.sleep(0.2)
                        running_ids = self.get_running_routines()

                while MicroState.routine_ongoing == True:
                    time.sleep(0.5)
                
                if MicroState.master_stop == False:
                    running_ids = self.get_running_routines()
                    if indexar_id not in running_ids:
                        print('RUTINA INDEXAR')
                        RoutineHandler(indexar_id).start()
                    
                    while indexar_id not in running_ids:
                        time.sleep(0.5)
                        running_ids = self.get_running_routines()
                
                while indexar_id in running_ids:
                    time.sleep(0.5)
                    running_ids = self.get_running_routines()
                
                MicroState.iteration += 1
                if MicroState.iteration > 2:
                    MicroState.iteration = 2
                
                if MicroState.master_stop == True:
                    MicroState.master_running = False
        
        return JsonResponse({})
    
    def get_running_routines(self):
        running_routines = []
        for routine in RoutineInfo.objects.all():
            if routine.running == 1:
                running_routines.append(ctrl_vars.ROUTINE_IDS[routine.name])
        return running_routines