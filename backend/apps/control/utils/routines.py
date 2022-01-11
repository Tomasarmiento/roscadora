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
    
    def run(self):
        self.routine_carga()
    
    def routine_giro_de_plato(self):
        # Paso 0 - Chequear condiciones iniciales
        init_flags = [
            ws_vars.MicroState.rem_i_states[1]['clampeo_plato_expandido'],      # plato_clampeado
            ws_vars.MicroState.rem_i_states[1]['acople_lubric_contraido'],      # acople_lubricante_contraido
            ws_vars.MicroState.rem_i_states[0]['puntera_descarga_contraida'],   # puntera_descarga_contraida
            ws_vars.MicroState.rem_i_states[0]['puntera_carga_contraida']       # puntera_carga_contraida
        ]
        initials = self.check_initials(init_flags)
        if initials:
            # Paso 1 - Liberar plato
            key_1 = 'contraer_clampeo_plato'
            key_2 = 'expandir_clampeo_plato'
            self.send_pneumatic(key_1, 1, 1, key_2, 0)
            
            self.wait_for_remote_in_flag('clampeo_plato_contraido', 1)
            
            # Paso 2 - Sale de safe para encender el servo
            command = Commands.exit_safe
            axis = ctrl_vars.AXIS_IDS['carga']
            msg_id = self.get_message_id()
            header = build_msg(command, eje=axis, msg_id=msg_id)
            self.send_message(header)
            
            target_state = msg_app.StateMachine.EST_INITIAL
            self.wait_for_axis_state(target_state, axis)
            
            # Paso 3 - Avanza 120° al siguiente paso
            self.move_step_load_axis()

            # Paso 4 - Power off
            command = Commands.power_off
            msg_id = self.get_message_id()
            header = build_msg(command, eje=axis, msg_id=msg_id)
            self.send_message(header)
            
            self.wait_for_axis_state(msg_app.StateMachine.EST_SAFE, axis)
            
            # Paso 5 - Clampea plato
            key_1 = 'expandir_clampeo_plato'
            key_2 = 'contraer_clampeo_plato'
            group = 1
            self.send_pneumatic(key_1, group, 1, key_2, 0)
            
            self.wait_for_remote_in_flag('clampeo_plato_expandido', group)
            return

    def routine_carga(self):
        # Paso 0 - Chequear condiciones iniciales
        init_flags = [
            ws_vars.MicroState.rem_i_states[1]['clampeo_plato_expandido'],      # plato_clampeado
            ws_vars.MicroState.rem_i_states[1]['acople_lubric_contraido'],      # acople_lubricante_contraido
            ws_vars.MicroState.rem_i_states[0]['puntera_descarga_contraida'],   # puntera_descarga_contraida
            ws_vars.MicroState.rem_i_states[0]['puntera_carga_contraida']       # puntera_carga_contraida
        ]
        initials = self.check_initials(init_flags)
        if initials:
            pass

    def send_message(self, header, data=None):
        if self.ch_info:
            if data:
                send_message(header, self.ch_info, data)
            else:
                send_message(header, self.ch_info)
            return True
        self.stop()

    def get_message_id(self):
        msg_id = ws_vars.MicroState.last_rx_header.get_msg_id() + 1
        ws_vars.MicroState.msg_id = msg_id
        return msg_id

    def check_initials(self, flags):
        if False in flags:
            return False
        return True
        # if routine == ctrl_vars.ROUTINE_IDS['cerado']:
        #     pass
        
        # if routine == ctrl_vars.ROUTINE_IDS['carga']:
        #     micro_state = ws_vars.MicroState
        #     flags = []
        #     # plato_clampeado = micro_state.rem_i_states[1]['clampeo_plato_expandido']
        #     acople_lubricante_contraido = micro_state.rem_i_states[1]['acople_lubric_contraido']
        #     puntera_descarga_contraida = micro_state.rem_i_states[0]['puntera_descarga_contraida']
        #     puntera_carga_contraida = micro_state.rem_i_states[0]['puntera_carga_contraida']
        #     # print('plato_clampeado:', plato_clampeado)
        #     print('acople_lubricante_contraido:', acople_lubricante_contraido)
        #     print('puntera_descarga_contraida', puntera_descarga_contraida)
        #     print('puntera_carga_contraida', puntera_carga_contraida)
        #     # flags.append(plato_clampeado)
        #     flags.append(acople_lubricante_contraido)
        #     flags.append(puntera_descarga_contraida)
        #     flags.append(puntera_carga_contraida)
        #     if False in flags:
        #         return False
        #     return True
            
        # if routine == ctrl_vars.ROUTINE_IDS['descarga']:
        #     pass
        
        # if routine == ctrl_vars.ROUTINE_IDS['roscado']:
        #     pass

    def send_pneumatic(self, key, group, bool_value, second_key=None, second_bool_value=None):
        command = Commands.rem_do_set
        header, data = ctrl_fun.set_rem_do(command, key, group, bool_value)
        self.send_message(header, data)
        if second_key:
            header, data = ctrl_fun.set_rem_do(command, second_key, group, second_bool_value)
            return self.send_message(header, data)
    
    def wait_for_remote_in_flag(self, flag_key, group):
        flag = ws_vars.MicroState.rem_i_states[group][flag_key]
        while not flag:     # Verifica que el plato está liberado
            flag = ws_vars.MicroState.rem_i_states[group][flag_key]
            time.sleep(self.wait_time)
        if not flag:
            self.stop()
        return True
    
    def wait_for_axis_state(self, target_state, axis):
        current_state_value = ws_vars.MicroState.axis_flags[axis]['maq_est_val']
        while current_state_value != target_state:
            current_state_value = ws_vars.MicroState.axis_flags[axis]['maq_est_val']
            time.sleep(self.wait_time)
        if current_state_value != target_state:
            self.stop()
        return True

    def move_step_load_axis(self):
        axis = ctrl_vars.AXIS_IDS['carga']
        pos = ws_vars.MicroState.axis_measures[axis]['pos_fil']
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
        msg_id = self.get_message_id()
        header, data = build_msg(command, ref=nex_step, ref_rate=ctrl_vars.COMMAND_REF_RATES['vel_carga'], msg_id=msg_id, eje=axis)

        self.send_message(header, data)
        
        pos = ws_vars.MicroState.axis_measures[axis]['pos_fil']
        print("POS:", pos)
        while not (pos >= nex_step - 1 and pos <= nex_step + 1):
            pos = ws_vars.MicroState.axis_measures[axis]['pos_fil']
            time.sleep(self.wait_time)

        self.wait_for_axis_state(msg_app.StateMachine.EST_INITIAL, axis)

    def stop(self):
        self._stop_event.set()
    
    def stopped(self):
        return self._stop_event.it_set()