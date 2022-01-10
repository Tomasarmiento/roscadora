import threading
import time

from apps.control.models import RoutineInfo
from apps.control.utils import functions as ctrl_fun
from apps.control.utils import variables as ctrl_vars

from apps.service.api.variables import Commands, COMMANDS
from apps.service.acdp.handlers import build_msg
from apps.service.acdp import messages_app as msg_app

from apps.ws.models import ChannelInfo
from apps.ws.utils import variables as ws_vars
from apps.ws.utils.handlers import send_message
from apps.ws.utils.functions import get_ch_info

class RoutineHandler(threading.Thread):

    def __init__(self, **kwargs):
        self.running_routines = []
        self.runnng_routines = ctrl_fun.get_running_routines(RoutineInfo)
        self.ch_info = get_ch_info(ChannelInfo, 'micro')
        super(RoutineHandler, self).__init__(**kwargs)
        self._stop_event = threading.Event()
        self.wait_time = 0.1
    
    def run(self) -> None:
        self.routine_carga()
    
    def routine_carga(self):
        initials = self.check_initials(ctrl_vars.ROUTINE_IDS['carga'])
        if initials:
            # Paso 1 - Liberar plato
            key = 'contraer_clampeo_plato'
            command = Commands.rem_do_set
            header, data = ctrl_fun.set_rem_do(command, key, 1, 1)

            if self.ch_info:
                send_message(header, self.ch_info, data)

            key = 'expandir_clampeo_plato'
            command = Commands.rem_do_set
            header, data = ctrl_fun.set_rem_do(command, key, 1, 0)

            if self.ch_info:
                send_message(header, self.ch_info, data)
            
            flag = ws_vars.MicroState.rem_i_states[1]['clampeo_plato_contraido']

            while not flag:     # Verifica que el plato está liberado
                flag = ws_vars.MicroState.rem_i_states[1]['clampeo_plato_contraido']
                time.sleep(self.wait_time)

            if not flag:
                return
            
            # Paso 2 - Sale de safe para encender el servo
            command = Commands.exit_safe
            axis = ctrl_vars.AXIS_IDS['carga']
            msg_id = ws_vars.MicroState.last_rx_header.get_msg_id() + 1
            ws_vars.MicroState.msg_id = msg_id
            header = build_msg(command, eje=axis, msg_id=msg_id)

            if self.ch_info:
                send_message(header, self.ch_info)
            
            state_value = ws_vars.MicroState.axis_flags[axis]['maq_est_val']

            while state_value != msg_app.StateMachine.EST_INITIAL:
                state_value = ws_vars.MicroState.axis_flags[axis]['maq_est_val']
                time.sleep(self.wait_time)
            
            # Paso 3 - Avanza 120° al siguiente paso
            pos = ws_vars.MicroState.eje_carga['pos_fil']
            steps = ctrl_vars.LOAD_STEPS
            current_step = None
            nex_step = None
            steps_count = len(steps)
            for i in range(steps_count):
                step = steps[i]
                if pos <= step + 2 and pos >= step - 2:
                    current_step = i
                    break
            if current_step == steps_count - 1:
                nex_step = 0
            else:
                nex_step = steps[current_step + 1]
            command = Commands.mov_to_pos
            msg_id = ws_vars.MicroState.last_rx_header.get_msg_id() + 1
            ws_vars.MicroState.msg_id = msg_id
            header, data = build_msg(command, ref=nex_step, ref_rate=ctrl_vars.COMMAND_REF_RATES['vel_carga'], msg_id=msg_id, eje=axis)

            if self.ch_info:
                send_message(header, self.ch_info, data)
            
            pos = ws_vars.MicroState.eje_carga['pos_fil']
            print("POS:", pos)
            while not (pos >= nex_step - 1 and pos <= nex_step + 1):
                pos = ws_vars.MicroState.eje_carga['pos_fil']
                time.sleep(self.wait_time)

            while state_value != msg_app.StateMachine.EST_INITIAL:
                state_value = ws_vars.MicroState.axis_flags[axis]['maq_est_val']
                time.sleep(self.wait_time)

            # Paso 4 - Power off
            command = Commands.power_off
            axis = ctrl_vars.AXIS_IDS['carga']
            msg_id = ws_vars.MicroState.last_rx_header.get_msg_id() + 1
            ws_vars.MicroState.msg_id = msg_id
            header = build_msg(command, eje=axis, msg_id=msg_id)

            if self.ch_info:
                send_message(header, self.ch_info)
            
            state_value = ws_vars.MicroState.axis_flags[axis]['maq_est_val']
            while state_value != msg_app.StateMachine.EST_SAFE:
                state_value = ws_vars.MicroState.axis_flags[axis]['maq_est_val']
                time.sleep(self.wait_time)
            
            # Paso 5 - Clampea plato
            key = 'expandir_clampeo_plato'
            command = Commands.rem_do_set
            header, data = ctrl_fun.set_rem_do(command, key, 1, 1)

            if self.ch_info:
                send_message(header, self.ch_info, data)

            key = 'contraer_clampeo_plato'
            command = Commands.rem_do_set
            header, data = ctrl_fun.set_rem_do(command, key, 1, 0)

            if self.ch_info:
                send_message(header, self.ch_info, data)
            
            flag = ws_vars.MicroState.rem_i_states[1]['clampeo_plato_expandido']

            while not flag:     # Verifica que el plato está liberado
                flag = ws_vars.MicroState.rem_i_states[1]['clampeo_plato_expandido']
                time.sleep(self.wait_time)

            if not flag:
                return

    def check_initials(self, routine):
        if routine == ctrl_vars.ROUTINE_IDS['cerado']:
            pass
        
        if routine == ctrl_vars.ROUTINE_IDS['carga']:
            micro_state = ws_vars.MicroState
            flags = []
            # plato_clampeado = micro_state.rem_i_states[1]['clampeo_plato_expandido']
            acople_lubricante_contraido = micro_state.rem_i_states[1]['acople_lubric_contraido']
            puntera_descarga_contraida = micro_state.rem_i_states[0]['puntera_descarga_contraida']
            puntera_carga_contraida = micro_state.rem_i_states[0]['puntera_carga_contraida']
            # print('plato_clampeado:', plato_clampeado)
            print('acople_lubricante_contraido:', acople_lubricante_contraido)
            print('puntera_descarga_contraida', puntera_descarga_contraida)
            print('puntera_carga_contraida', puntera_carga_contraida)
            # flags.append(plato_clampeado)
            flags.append(acople_lubricante_contraido)
            flags.append(puntera_descarga_contraida)
            flags.append(puntera_carga_contraida)
            if False in flags:
                return False
            return True
            
        if routine == ctrl_vars.ROUTINE_IDS['descarga']:
            pass
        
        if routine == ctrl_vars.ROUTINE_IDS['roscado']:
            pass

    def stop(self):
        self._stop_event.set()
    
    def stopped(self):
        return self._stop_event.it_set()