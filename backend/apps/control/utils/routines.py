import threading
import time
from datetime import datetime

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

    def __init__(self, routine=None, **kwargs):
        self.running_routines = []
        self.runnng_routines = ctrl_fun.get_running_routines(RoutineInfo)
        self.current_routine = routine
        self.ch_info = get_ch_info(ChannelInfo, 'micro')
        super(RoutineHandler, self).__init__(**kwargs)
        self._stop_event = threading.Event()
        self.wait_time = 0.1
    
    def run(self):
        routine = self.current_routine
        if routine:
            routine_ok = None
            start_time = datetime.now()
            if routine == ctrl_vars.ROUTINE_IDS['cabezal_indexar']:
                print('ROUTINE CABEZAL')
                routine_ok = self.routine_cabezal_indexar()
            
            elif routine == ctrl_vars.ROUTINE_IDS['carga']:
                print('CARGA')
                routine_ok = self.routine_carga()
            
            elif routine == ctrl_vars.ROUTINE_IDS['descarga']:
                print('DESCARGA')
                routine_ok = self.routine_descarga()
            
            end_time = datetime.now()
            print('ROUTINE TIME:', end_time - start_time)
            if routine_ok:
                print('Routine OK')
                return True
            else:
                print('ROUTINE ERR')
                return False
        else:
            print('Rutine no especificada')
    
    def routine_cabezal_indexar(self):
        # Paso 0 - Chequear condiciones iniciales
        init_flags = [
            ws_vars.MicroState.rem_i_states[1]['clampeo_plato_expandido'],      # plato_clampeado
            ws_vars.MicroState.rem_i_states[1]['acople_lubric_contraido'],      # acople_lubricante_contraido
            ws_vars.MicroState.rem_i_states[0]['puntera_descarga_contraida'],   # puntera_descarga_contraida
            ws_vars.MicroState.rem_i_states[0]['puntera_carga_contraida']       # puntera_carga_contraida
        ]
        print(init_flags)
        if False in init_flags:
            return
        # Paso 1 - Liberar plato
        key_1 = 'contraer_clampeo_plato'
        key_2 = 'expandir_clampeo_plato'
        if not self.send_pneumatic(key_1, 1, 1, key_2, 0):
            return False
        
        if not self.wait_for_remote_in_flag('clampeo_plato_contraido', 1):
            return False
        
        # Paso 2 - Sale de safe para encender el servo
        command = Commands.exit_safe
        axis = ctrl_vars.AXIS_IDS['carga']
        msg_id = self.get_message_id()
        header = build_msg(command, eje=axis, msg_id=msg_id)
        if not self.send_message(header):
            return False
        
        target_state = msg_app.StateMachine.EST_INITIAL
        if not self.wait_for_axis_state(target_state, axis):
            return False
        
        # Paso 3 - Avanza 120° al siguiente paso
        if not self.move_step_load_axis():
            return False

        # Paso 4 - Power off
        command = Commands.power_off
        msg_id = self.get_message_id()
        header = build_msg(command, eje=axis, msg_id=msg_id)
        if not self.send_message(header):
            return False
        
        if not self.wait_for_axis_state(msg_app.StateMachine.EST_SAFE, axis):
            return False
        
        # Paso 5 - Clampea plato
        key_1 = 'expandir_clampeo_plato'
        key_2 = 'contraer_clampeo_plato'
        group = 1
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        
        if not self.wait_for_remote_in_flag('clampeo_plato_expandido', group):
            return False
        return True

    def routine_carga(self):
        # Paso 0 - Chequear condiciones iniciales - Todos los valores deben ser True par que empiece la rutina
        init_flags = [
            ws_vars.MicroState.rem_o_states[1]['encender_bomba_hidraulica'],        # hidráulica ON
            ws_vars.MicroState.rem_i_states[1]['clampeo_plato_expandido'],          # Plato clampeado
            ws_vars.MicroState.rem_i_states[0]['vertical_carga_contraido'],         # vertical_carga_contraido
            ws_vars.MicroState.rem_i_states[0]['puntera_carga_contraida'],          # puntera_carga_contraida
            ws_vars.MicroState.rem_i_states[0]['brazo_cargador_expandido'],         # brazo_cargador_expandido
            ws_vars.MicroState.rem_i_states[0]['boquilla_carga_expandida'],         # ws_vars.MicroState.rem_i_states[0]
            ws_vars.MicroState.rem_i_states[1]['presencia_cupla_en_cargador'],      # presencia_cupla_en_cargador
            not ws_vars.MicroState.rem_i_states[1]['pieza_en_boquilla_carga']       # pieza_en_boquilla_carga
        ]
        print(init_flags)
        if False in init_flags:
            return
        
        # Paso 1 - Expandir vertical carga
        key = 'expandir_vertical_carga'
        wait_key = 'vertical_carga_expandido'
        group = 0
        wait_group = 0
        if not self.send_pneumatic(key, group, 1):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False

        # Paso 2 - Expandir puntera carga
        key_1 = 'expandir_puntera_carga'
        key_2 = 'contraer_puntera_carga'
        wait_key = 'puntera_carga_expandida'
        group = 0
        print("EXPANDIR PUNTERA CARGA")
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        
        # Paso 3 - Boquilla carga contraida
        key = 'contraer_boquilla_carga'
        wait_key = 'boquilla_carga_contraida'
        group = 0
        wait_group = 0
        if not self.send_pneumatic(key, group, 1):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        
        # Paso 4 - Verificar flags pieza en boquilla carga
        key = 'pieza_en_boquilla_carga'
        if not ws_vars.MicroState.rem_i_states[1][key]:
            return False
        else:
            print("PIEZA EN BOQUILLA", ws_vars.MicroState.rem_i_states[1][key])
        # Paso 5 - Puntera cargador contraída
        key_1 = 'contraer_puntera_carga'
        key_2 = 'expandir_puntera_carga'
        wait_key = 'puntera_carga_contraida'
        group = 0
        wait_group = 0
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        
        # Paso 6 - Contraer vertical y brazo cargador
        key = 'expandir_vertical_carga'
        group = 0
        if not self.send_pneumatic(key, group, 0):
            return False
        key_1 = 'contraer_brazo_cargador'
        key_2 = 'expandir_brazo_cargador'
        group = 0
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        
        wait_key = 'vertical_carga_contraido'
        wait_group = 0
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print('VERTICAL CARGA CONTRAIDO')
        wait_key = 'brazo_cargador_contraido'
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print('BRAZO CARGA CONTRAIDO')
        
        # Paso 7 - Verificar pieza en boquilla carga
        if not ws_vars.MicroState.rem_i_states[1]['pieza_en_boquilla_carga']:
            return False
        else:
            print('PIEZA EN BOQUILLA CARGA')
        
        # Paso 8 - Avanza puntera carga en boquilla
        key_1 = 'expandir_puntera_carga'
        key_2 = 'contraer_puntera_carga'
        wait_key = 'puntera_carga_contraida'
        group = 0
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        if not self.wait_for_not_remote_in_flag(wait_key, wait_group):
            return False
        time.sleep(1)
        print('PUNTERA EXPANDIDA')
        
        # Paso 9 - Boquilla carga extendida
        key = 'contraer_boquilla_carga'
        wait_key = 'boquilla_carga_expandida'
        group = 0
        wait_group = 0
        if not self.send_pneumatic(key, group, 0):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print("BOQUILLA CARGA CONTRAIDA")
        # Paso 10 - Presurizar ON
        key = 'presurizar'
        group = 1
        self.send_pneumatic(key, group, 1)
        print('PRESURIZAR')
        
        # Paso 11 - Contraer boquilla cabezal
        boquilla = self.get_current_boquilla_carga()
        key_1 = 'cerrar_boquilla_' + str(boquilla)
        key_2 = 'abrir_boquilla_' + str(boquilla)
        group = 1
        self.send_pneumatic(key_1, group, 1, key_2, 0)
        time.sleep(2)

        # Paso 12 - Puntera cargador contraída
        key_1 = 'contraer_puntera_carga'
        key_2 = 'expandir_puntera_carga'
        wait_key = 'puntera_carga_contraida'
        group = 0
        wait_group = 0
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print("CONTRAER BOQUILLA CABEZAL")

        # Paso 13 - Verificar pieza en boquilla carga
        if ws_vars.MicroState.rem_i_states[1]['pieza_en_boquilla_carga']:
            return False
        print('CUPLA NO PRESENTE')

        # Paso 14 - Cerrar válvula de boquilla hidráulica
        boquilla = self.get_current_boquilla_carga()
        key_1 = 'cerrar_boquilla_' + str(boquilla)
        key_2 = 'abrir_boquilla_' + str(boquilla)
        group = 1
        self.send_pneumatic(key_1, group, 0, key_2, 0)
        print('CERRAR VALVULA HIDRAULICA')

        # Paso 15 - Presurizar OFF
        key = 'presurizar'
        group = 1
        self.send_pneumatic(key, group, 0)
        print('PRESURIZAR OFF')

        # Paso 16 - Expandir brazo cargador
        key_1 = 'expandir_brazo_cargador'
        key_2 = 'contraer_brazo_cargador'
        wait_key = 'brazo_cargador_expandido'
        group = 0
        wait_group = 0
        
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print('FIN RUTINA CARGA') 
        return True

    def routine_descarga(self):
        # Paso 0 - Chequear condiciones iniciales - Todos los valores deben ser True par que empiece la rutina
        init_flags = [
            ws_vars.MicroState.rem_o_states[1]['encender_bomba_hidraulica'],        # hidráulica ON
            ws_vars.MicroState.rem_i_states[1]['clampeo_plato_expandido'],          # Plato clampeado
            ws_vars.MicroState.rem_i_states[0]['puntera_descarga_contraida'],       # puntera_descarga_contraida
            ws_vars.MicroState.rem_i_states[0]['brazo_descarga_expandido'],         # brazo_descarga_expandido
            ws_vars.MicroState.rem_i_states[0]['boquilla_descarga_expandida'],      # boquilla_descarga_expandida
            ws_vars.MicroState.rem_i_states[1]['cupla_por_tobogan_descarga'],       # cupla_por_tobogan_descarga
            not ws_vars.MicroState.rem_i_states[1]['pieza_en_boquilla_descarga'],   # pieza_en_boquilla_descarga
            ws_vars.MicroState.rem_i_states[1]['horiz_pinza_desc_contraido'],       # horiz_pinza_desc_contraido
            ws_vars.MicroState.rem_i_states[1]['vert_pinza_desc_contraido'],        # vert_pinza_desc_contraido
            ws_vars.MicroState.rem_i_states[0]['pinza_descargadora_abierta']        # pinza_descargadora_abierta
        ]
        print(init_flags)
        if False in init_flags:
            return
        
        # Paso 1 - Expandir puntera descarga
        key_1 = 'expandir_puntera_descarga'
        key_2 = 'contraer_puntera_descarga'
        wait_key = 'puntera_descarga_contraida'
        group = 0
        wait_group = 0
        print("EXPANDIR PUNTERA DESCARGA")
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        if not self.wait_for_not_remote_in_flag(wait_key, wait_group):
            return False
        time.sleep(1)

        # Paso 2 - Boquilla descarga contraida
        key = 'contraer_boquilla_descarga'
        wait_key = 'boquilla_descarga_expandida'
        group = 0
        wait_group = 0
        if not self.send_pneumatic(key, group, 1):
            return False
        if not self.wait_for_not_remote_in_flag(wait_key, wait_group):
            return False
        time.sleep(1)
        print('contraer_boquilla_descarga')

        # Paso 3 - Presurizar OFF
        key = 'presurizar'
        group = 1
        self.send_pneumatic(key, group, 0)
        print('PRESURIZAR OFF')

        # Paso 4 - Abrir válvula de boquilla hidráulica
        boquilla = self.get_current_boquilla_descarga()
        key_1 = 'abrir_boquilla_' + str(boquilla)
        key_2 = 'cerrar_boquilla_' + str(boquilla)
        group = 1
        self.send_pneumatic(key_1, group, 1, key_2, 0)
        print('CERRAR VALVULA HIDRAULICA')
        time.sleep(2)

        # Paso 5 - Puntera descargador contraída
        key_1 = 'contraer_puntera_descarga'
        key_2 = 'expandir_puntera_descarga'
        wait_key = 'puntera_descarga_contraida'
        group = 0
        wait_group = 0
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print("PUNTERA DESCARGA CONTRAIDA")

        # Paso 6 - Verificar pieza en boquilla descarga
        if not ws_vars.MicroState.rem_i_states[1]['pieza_en_boquilla_descarga']:
            return False
        print('CUPLA PRESENTE')

        # Paso 7 - Contraer brazo descargador
        key_1 = 'contraer_brazo_descargador'
        key_2 = 'expandir_brazo_descargador'
        wait_key = 'brazo_descarga_contraido'
        group = 0
        wait_group = 0
        
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        
        # Paso 8 - Expandir puntera descarga
        key_1 = 'expandir_puntera_descarga'
        key_2 = 'contraer_puntera_descarga'
        wait_key = 'puntera_descarga_expandida'
        group = 0
        wait_group = 0
        print("EXPANDIR PUNTERA DESCARGA")
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        
        # Paso 9 - Verificar pieza en boquilla descarga
        if not ws_vars.MicroState.rem_i_states[1]['pieza_en_boquilla_descarga']:
            return False
        print('CUPLA PRESENTE')

        # Paso 10 - expandir_horiz_pinza_desc
        key = 'expandir_horiz_pinza_desc'
        group = 1
        wait_key = 'horiz_pinza_desc_expandido'
        wait_group = 1
        if not self.send_pneumatic(key, group, 1):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print('PASO 10')
        print('expandir_horiz_pinza_desc')

        # Paso 11 - expandir_vert_pinza_desc
        key = 'expandir_vert_pinza_desc'
        group = 1
        wait_key = 'vert_pinza_desc_expandido'
        wait_group = 1
        if not self.send_pneumatic(key, group, 1):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print('PASO 11')
        print('expandir_vert_pinza_desc')

        # Paso 12 - pinza_descargadora_cerrada
        key_1 = 'cerrar_pinza_descargadora'
        key_2 = 'abrir_pinza_descargadora'
        group = 0
        wait_key = 'pinza_descargadora_abierta'
        wait_group = 0
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        if not self.wait_for_not_remote_in_flag(wait_key, wait_group):
            return False
        time.sleep(1)
        print('PASO 12')
        print('pinza_descargadora_cerrada')

        # Paso 13 - Boquilla descarga expandir
        key = 'contraer_boquilla_descarga'
        wait_key = 'boquilla_descarga_expandida'
        group = 0
        wait_group = 0
        if not self.send_pneumatic(key, group, 0):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        time.sleep(1)
        print('PASO 13')
        print('Boquilla descarga expandir')

        # Paso 14 - Puntera descargador contraída
        key_1 = 'contraer_puntera_descarga'
        key_2 = 'expandir_puntera_descarga'
        wait_key = 'puntera_descarga_contraida'
        group = 0
        wait_group = 0
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print('PASO 14')
        print("PUNTERA DESCARGA CONTRAIDA")

        # Paso 15 - Verificar pieza no presente en boquilla descarga
        if ws_vars.MicroState.rem_i_states[1]['pieza_en_boquilla_descarga']:
            return False
        print('PASO 15')
        print('Verificar pieza no presente en boquilla descarga')
        
        # Paso 16 - Expandir brazo descargador
        key_1 = 'expandir_brazo_descargador'
        key_2 = 'contraer_brazo_descargador'
        wait_key = 'brazo_descarga_expandido'
        group = 0
        wait_group = 0
        
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print('PASO 16')

        # Paso 17 - contraer_vert_pinza_desc
        key = 'expandir_vert_pinza_desc'
        group = 1
        wait_key = 'vert_pinza_desc_contraido'
        wait_group = 1
        if not self.send_pneumatic(key, group, 0):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print('PASO 17')
        print('contraer_vert_pinza_desc')

        # Paso 18 - contraer_horiz_pinza_desc
        key = 'expandir_horiz_pinza_desc'
        group = 1
        wait_key = 'horiz_pinza_desc_contraido'
        wait_group = 1
        if not self.send_pneumatic(key, group, 0):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print('PASO 18')
        print('contraer_horiz_pinza_desc')

        # Paso 19 - expandir_vert_pinza_desc
        key = 'expandir_vert_pinza_desc'
        group = 1
        wait_key = 'vert_pinza_desc_expandido'
        wait_group = 1
        if not self.send_pneumatic(key, group, 1):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print('PASO 19')
        print('expandir_vert_pinza_desc')

        # Paso 20 - pinza_descargadora_abierta
        key_1 = 'abrir_pinza_descargadora'
        key_2 = 'cerrar_pinza_descargadora'
        group = 0
        wait_key = 'pinza_descargadora_abierta'
        wait_group = 0
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print('PASO 20')
        print('pinza_descargadora_abierta')

        # Paso 21 - contraer_vert_pinza_desc
        key = 'expandir_vert_pinza_desc'
        group = 1
        wait_key = 'vert_pinza_desc_contraido'
        wait_group = 1
        if not self.send_pneumatic(key, group, 0):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print('PASO 21')
        print('contraer_vert_pinza_desc')

        # Paso 22 - Expera presencia de cupla en tobogan
        flag = ws_vars.MicroState.rem_i_states[1]['cupla_por_tobogan_descarga']
        while flag:
            flag = ws_vars.MicroState.rem_i_states[1]['cupla_por_tobogan_descarga']
            time.sleep(self.wait_time)
        print('FIN RUTINA DESCARGA')

        return True

    def send_message(self, header, data=None):
        if self.ch_info:
            if data:
                send_message(header, self.ch_info, data)
            else:
                send_message(header, self.ch_info)
            return True
        return False

    def get_message_id(self):
        msg_id = ws_vars.MicroState.last_rx_header.get_msg_id() + 1
        ws_vars.MicroState.msg_id = msg_id
        return msg_id

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

    def send_pneumatic(self, key, group, bool_value, second_key=None, second_bool_value=None):
        command = Commands.rem_do_set
        header, data = ctrl_fun.set_rem_do(command, key, group, bool_value)
        if not self.send_message(header, data):
            return False
        if second_key:
            header, data = ctrl_fun.set_rem_do(command, second_key, group, second_bool_value)
            return self.send_message(header, data)
        return True
    
    def wait_for_remote_in_flag(self, flag_key, group):
        flag = ws_vars.MicroState.rem_i_states[group][flag_key]
        while not flag:     # Verifica que el flag está en HIGH
            flag = ws_vars.MicroState.rem_i_states[group][flag_key]
            time.sleep(self.wait_time)
        if not flag:
            return False
        return True
    
    def wait_for_not_remote_in_flag(self, flag_key, group):
        flag = ws_vars.MicroState.rem_i_states[group][flag_key]
        while flag:     # Verifica que el flag está en LOW
            flag = ws_vars.MicroState.rem_i_states[group][flag_key]
            time.sleep(self.wait_time)
        if flag:
            return False
        return True
    
    def wait_for_axis_state(self, target_state, axis):
        current_state_value = ws_vars.MicroState.axis_flags[axis]['maq_est_val']
        while current_state_value != target_state:
            current_state_value = ws_vars.MicroState.axis_flags[axis]['maq_est_val']
            time.sleep(self.wait_time)
        if current_state_value != target_state:
            return False
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

        if not self.send_message(header, data):
            return False
        
        pos = ws_vars.MicroState.axis_measures[axis]['pos_fil']
        print("POS:", pos)
        while not (pos >= nex_step - 1 and pos <= nex_step + 1):
            pos = ws_vars.MicroState.axis_measures[axis]['pos_fil']
            time.sleep(self.wait_time)

        return self.wait_for_axis_state(msg_app.StateMachine.EST_INITIAL, axis)

    def get_current_boquilla_carga(self):
        axis = ctrl_vars.AXIS_IDS['carga']
        pos = ws_vars.MicroState.axis_measures[axis]['pos_fil']
        steps = ctrl_vars.LOAD_STEPS
        current_step = -1
        steps_count = len(steps)
        for i in range(steps_count):
            step = steps[i]
            if pos <= step + 2 and pos >= step - 2:
                current_step = i
                break
        if current_step >= 0:
            return ctrl_vars.BOQUILLA_CARGADOR[current_step]
        return False
    
    def get_current_boquilla_descarga(self):
        axis = ctrl_vars.AXIS_IDS['carga']
        pos = ws_vars.MicroState.axis_measures[axis]['pos_fil']
        steps = ctrl_vars.LOAD_STEPS
        current_step = -1
        steps_count = len(steps)
        print("POS", pos)
        for i in range(steps_count):
            step = steps[i]
            if pos <= step + 2 and pos >= step - 2:
                current_step = i
                break
        print("CURRENT STEP:", current_step)
        if current_step >= 0:
            return ctrl_vars.BOQUILLA_DESCARGADOR[current_step]
        return False

    def stop(self):
        self._stop_event.set()
    
    def stopped(self):
        return self._stop_event.it_set()