import threading
import time
from datetime import datetime

from apps.control.models import RoutineInfo
from apps.control.utils import functions as ctrl_fun
from apps.control.utils import variables as ctrl_vars

from apps.service.api.variables import Commands, COMMANDS
from apps.service.acdp.handlers import build_msg
from apps.service.acdp import messages_app as msg_app
from apps.service.acdp import messages_base as msg_base

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
        self.wait_time = 0.05
        self.err_msg = []
    

    def run(self):
        routine = self.current_routine
        print('INICIO DE RUTINA ID', routine)
        if routine:
            routine_ok = None
            
            start_time = datetime.now()
            pos = round(ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['carga']]['pos_fil'], 0)
            
            try:
                routine_info = RoutineInfo.objects.get(name=ctrl_vars.ROUTINE_NAMES[routine])
                print('RUTINA', ctrl_vars.ROUTINE_NAMES[routine])
            except RoutineInfo.DoesNotExist:
                print('ID de rutina inválido')
                return False

            if routine_info.running == 1:
                print('La rutina ya se está ejecutando')
                return False
            
            self.set_routine_ongoing_flag()

            if routine == ctrl_vars.ROUTINE_IDS['cerado']:
                if ws_vars.MicroState.routine_ongoing == True:
                    print('Rutina en proceso. No se puede cerar')
                    return False
                print('CERADO')
                ws_vars.MicroState.routine_ongoing = True
                routine_info.running = 1
                routine_info.save()
                routine_ok = self.routine_homing()
            
            elif pos not in ctrl_vars.LOAD_STEPS:
                routine_ok = False
                print('Error en posicion de cabezal')
            
            elif ws_vars.MicroState.rem_i_states[1]['presion_normal'] == False:
                routine_ok = False
                print('Baja presión')
            
            elif routine == ctrl_vars.ROUTINE_IDS['cabezal_indexar']:
                if ws_vars.MicroState.routine_ongoing == True:
                    print('Rutina en proceso. No se puede indexar')
                    return False
                ws_vars.MicroState.routine_ongoing = True
                routine_info.running = 1
                routine_info.save()
                print('ROUTINE CABEZAL')
                routine_ok = self.routine_cabezal_indexar()

            else:
                routine_info.running = 1
                routine_info.save()
                ws_vars.MicroState.routine_ongoing = True
                
                if routine == ctrl_vars.ROUTINE_IDS['carga']:
                    print('CARGA')
                    routine_ok = self.routine_carga()
                
                elif routine == ctrl_vars.ROUTINE_IDS['descarga']:
                    print('DESCARGA')
                    routine_ok = self.routine_descarga()
                
                elif routine == ctrl_vars.ROUTINE_IDS['roscado']:
                    print('ROSCADO')
                    routine_ok = self.routine_roscado()
            
            routine_info.running = 0
            routine_info.save()
            end_time = datetime.now()
            ws_vars.MicroState.routine_ongoing = self.check_running_routines()
            if routine_ok:
                print('Routine OK')
                print('ROUTINE TIME:', end_time - start_time)
                return True
            else:
                print('ROUTINE ERR')
                ws_vars.MicroState.master_stop = True
                for msg in self.err_msg:
                    print(msg)
                return False
        else:
            print('Rutina no especificada')
    

    def routine_cabezal_indexar(self):
        # Paso 0 - Chequear condiciones iniciales
        eje_avance = ctrl_vars.AXIS_IDS['avance']
        init_flags = [
            ws_vars.MicroState.rem_i_states[1]['clampeo_plato_expandido'],      # plato_clampeado
            ws_vars.MicroState.rem_i_states[1]['acople_lubric_contraido'],      # acople_lubricante_contraido
            ws_vars.MicroState.rem_i_states[0]['puntera_descarga_contraida'],   # puntera_descarga_contraida
            ws_vars.MicroState.rem_i_states[0]['puntera_carga_contraida'],      # puntera_carga_contraida
            round(ws_vars.MicroState.axis_measures[eje_avance]['pos_fil'], 0) == round(ctrl_vars.ROSCADO_CONSTANTES['posicion_de_inicio'], 0)   # Eje avance en posición de inicio
        ]
        print('Paso 0 - Chequear condiciones iniciales')
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
        print('Paso 1 - Liberar plato')


        # Paso 2 - Power on servo carga
        command = Commands.power_on
        axis = ctrl_vars.AXIS_IDS['carga']
        msg_id = self.get_message_id()
        header = build_msg(command, eje=axis, msg_id=msg_id)
        if not self.send_message(header):
            return False
    
        if not self.wait_for_axis_state(msg_app.StateMachine.EST_INITIAL, axis):
            return False
        print(' Paso 5 - Power on servo carga')
       

        # Paso 3 - Avanza 120° al siguiente paso
        turn_init_flags = [
            ws_vars.MicroState.rem_i_states[1]['acople_lubric_contraido'],      # acople_lubricante_contraido
            ws_vars.MicroState.rem_i_states[0]['puntera_descarga_contraida'],   # puntera_descarga_contraida
            ws_vars.MicroState.rem_i_states[0]['puntera_carga_contraida'],      # puntera_carga_contraida
            round(ws_vars.MicroState.axis_measures[eje_avance]['pos_fil'], 0) == round(ctrl_vars.ROSCADO_CONSTANTES['posicion_de_inicio'], 0)   # Eje avance en posición de inicio
        ]

        if False in turn_init_flags:
            self.err_msg.append('Error en condiciones de giro indexado')
            return False

        if not self.move_step_load_axis():
            return False
        print(' Paso 3 - Avanza 120° al siguiente paso')


        # Paso 4 - Clampea plato
        key_1 = 'expandir_clampeo_plato'
        key_2 = 'contraer_clampeo_plato'
        group = 1
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        
        if not self.wait_for_remote_in_flag('clampeo_plato_expandido', group):
            return False
        print('Paso 4 - Clampea plato')


        # Paso 5 - Power off
        command = Commands.power_off
        msg_id = self.get_message_id()
        drv_flag = msg_base.DrvFbkDataFlags.ENABLED
        header = build_msg(command, eje=axis, msg_id=msg_id)
        if not self.send_message(header):
            return False
        
        if not self.wait_for_drv_flag(drv_flag, axis, 0):
            return False
        print(' Paso 5 - Power off')



        print('FIN RUTINA CABEZAL INDEXAR')
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
        print('Paso 1 - Expandir vertical carga')
        
        # Paso 1.1 - Abrir válvula de boquilla hidráulica
        boquilla = self.get_current_boquilla_carga()
        key_1 = 'cerrar_boquilla_' + str(boquilla)
        key_2 = 'abrir_boquilla_' + str(boquilla)
        group = 1
        self.send_pneumatic(key_1, group, 0, key_2, 1)
        print('Paso 1.1 - Abrir válvula de boquilla hidráulica')

        # Paso 2 - Expandir puntera carga
        key_1 = 'expandir_puntera_carga'
        key_2 = 'contraer_puntera_carga'
        wait_key = 'puntera_carga_contraida'
        group = 0
        print("EXPANDIR PUNTERA CARGA")
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        if not self.wait_for_not_remote_in_flag(wait_key, wait_group):
            return False
        time.sleep(1)
        print(' Paso 2 - Expandir puntera carga')

        # Paso 3 - Boquilla carga contraida
        key = 'contraer_boquilla_carga'
        wait_key = 'boquilla_carga_contraida'
        group = 0
        wait_group = 0
        if not self.send_pneumatic(key, group, 1):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print('Paso 3 - Boquilla carga contraida')
        
        # Paso 4 - Verificar flags pieza en boquilla carga
        key = 'pieza_en_boquilla_carga'
        if not ws_vars.MicroState.rem_i_states[1][key]:
            return False
        print("PIEZA EN BOQUILLA", ws_vars.MicroState.rem_i_states[1][key])
        print('Paso 4 - Verificar flags pieza en boquilla carga')

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
        print('Paso 5 - Puntera cargador contraída')

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
        print('Paso 6 - Contraer vertical y brazo cargador')

        # Paso 7 - Verificar pieza en boquilla carga
        if not ws_vars.MicroState.rem_i_states[1]['pieza_en_boquilla_carga']:
            return False
        else:
            print('PIEZA EN BOQUILLA CARGA')
        print(' Paso 7 - Verificar pieza en boquilla carga')

        # Paso 8 - Avanza puntera carga en boquilla
        key_1 = 'expandir_puntera_carga'
        key_2 = 'contraer_puntera_carga'
        wait_key = 'puntera_carga_contraida'
        group = 0

        load_init_flags = [
            ws_vars.MicroState.rem_i_states[1]['clampeo_plato_expandido'],          # Plato clampeado
        ]

        if False in load_init_flags:
            self.err_msg.append('Error en condiciones de avanzar puntera en boquilla durante carga')
            return False
        
        pos = round(ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['carga']]['pos_fil'], 0)
        if pos not in ctrl_vars.LOAD_STEPS:
            print('Error en posicion de cabezal')
            return False
        
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        if not self.wait_for_not_remote_in_flag(wait_key, wait_group):
            return False
        time.sleep(1)
        print('PUNTERA EXPANDIDA')
        print('Paso 8 - Avanza puntera carga en boquilla')

        # Paso 9 - Boquilla carga extendida
        key = 'contraer_boquilla_carga'
        wait_key = 'boquilla_carga_expandida'
        group = 0
        wait_group = 0
        if not self.send_pneumatic(key, group, 0):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print('Paso 9 - Boquilla carga extendida')

        # Paso 10 - Presurizar ON
        ws_vars.MicroState.load_allow_presure_off = False
        key = 'presurizar'
        group = 1
        self.send_pneumatic(key, group, 1)
        print('Paso 10 - Presurizar ON')
        
        # Paso 11 - Contraer boquilla cabezal
        boquilla = self.get_current_boquilla_carga()
        key_1 = 'cerrar_boquilla_' + str(boquilla)
        key_2 = 'abrir_boquilla_' + str(boquilla)
        group = 1
        self.send_pneumatic(key_1, group, 1, key_2, 0)
        time.sleep(2)
        print('Paso 11 - Contraer boquilla cabezal')

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
        print('Paso 12 - Puntera cargador contraída')

        # Paso 13 - Verificar pieza en boquilla carga
        if ws_vars.MicroState.rem_i_states[1]['pieza_en_boquilla_carga']:
            return False
        print('CUPLA NO PRESENTE')
        print('Paso 13 - Verificar pieza en boquilla carga')

        # Paso 14 - Cerrar válvula de boquilla hidráulica
        boquilla = self.get_current_boquilla_carga()
        key_1 = 'cerrar_boquilla_' + str(boquilla)
        key_2 = 'abrir_boquilla_' + str(boquilla)
        group = 1
        self.send_pneumatic(key_1, group, 0, key_2, 0)
        print('CERRAR VALVULA HIDRAULICA')
        print('Paso 14 - Cerrar válvula de boquilla hidráulica')
        time.sleep(1)

        # Paso 14.1 - Espera habilitación de presurizar off en roscado
        roscado_id = ctrl_vars.ROUTINE_IDS['roscado']
        roscado_running = (RoutineInfo.objects.get(name=ctrl_vars.ROUTINE_NAMES[roscado_id]).running == 1)
        print('ROSCADO EN PROCESO:', roscado_running)
        
        if roscado_running:
            if self.wait_presure_off_allowed(roscado_id) == False:
                return False

        # Paso 15 - Presurizar OFF
        ws_vars.MicroState.load_allow_presure_off = True
        key = 'presurizar'
        group = 1
        self.send_pneumatic(key, group, 0)
        print('Paso 15 - Presurizar OFF')

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
        print('Paso 16 - Expandir brazo cargador')

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
        
        # Paso 0.1 - expandir_horiz_pinza_desc
        key = 'expandir_horiz_pinza_desc'
        group = 1
        if not self.send_pneumatic(key, group, 1):
            return False
        print('expandir_horiz_pinza_desc')
        print('Paso 0.1')

        # Paso 1 - Expandir puntera descarga
        unload_init_flags = [
            ws_vars.MicroState.rem_i_states[1]['clampeo_plato_expandido'],          # Plato clampeado
        ]

        if False in unload_init_flags:
            self.err_msg.append('Error en condiciones de avanzar puntera en boquilla durante carga')
            return False
        
        pos = round(ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['carga']]['pos_fil'], 0)
        if pos not in ctrl_vars.LOAD_STEPS:
            print('Error en posicion de cabezal')
            return False

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
        time.sleep(2)
        print('Paso 1 - Expandir puntera descarga')

        # Paso 1.1 - Verifica paso 0.1
        wait_key = 'horiz_pinza_desc_expandido'
        wait_group = 1
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False

        # Paso 1.2 - expandir_vert_pinza_desc
        key = 'expandir_vert_pinza_desc'
        group = 1
        if not self.send_pneumatic(key, group, 1):
            return False
        print('PASO 1.1')

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

        # Paso 3 - Verifica paso 1.2
        wait_key = 'vert_pinza_desc_expandido'
        wait_group = 1
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print('expandir_vert_pinza_desc')

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

        # Paso 14.1 - contraer_vert_pinza_desc
        key = 'expandir_vert_pinza_desc'
        group = 1
        if not self.send_pneumatic(key, group, 0):
            return False
        print('Paso 14.1 - contraer_vert_pinza_desc')
        
        # Paso 15 - Verificar pieza no presente en boquilla descarga
        if ws_vars.MicroState.rem_i_states[1]['pieza_en_boquilla_descarga']:
            return False
        print('PASO 15')
        print('Verificar pieza no presente en boquilla descarga')
        
        # Paso 16 - Expandir brazo descargador
        key_1 = 'expandir_brazo_descargador'
        key_2 = 'contraer_brazo_descargador'
        group = 0
        
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        
        # Paso 16.1 - Verifica paso 14.1
        wait_key = 'vert_pinza_desc_contraido'
        wait_group = 1
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print('contraer_vert_pinza_desc')

        # Paso 16.2 - contraer_horiz_pinza_desc
        key = 'expandir_horiz_pinza_desc'
        group = 1
        wait_key = 'horiz_pinza_desc_contraido'
        wait_group = 1
        if not self.send_pneumatic(key, group, 0):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print('Paso 16.2 - contraer_horiz_pinza_desc')
        print('contraer_horiz_pinza_desc')

        # Paso 16.3 - Verifica paso 16
        wait_key = 'brazo_descarga_expandido'
        wait_group = 0
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print('PASO 16')

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


    def routine_roscado(self):
        eje_avance = ctrl_vars.AXIS_IDS['avance']
        eje_carga = ctrl_vars.AXIS_IDS['carga']
        initial_state = msg_app.StateMachine.EST_INITIAL
        safe_state = msg_app.StateMachine.EST_SAFE
        # Paso 0 - Chequear condiciones iniciales - Todos los valores deben ser True par que empiece la rutina
        init_flags = [
            ws_vars.MicroState.rem_o_states[1]['encender_bomba_hidraulica'],                                # hidráulica ON
            ws_vars.MicroState.rem_i_states[1]['clampeo_plato_expandido'],                                  # Plato clampeado
            ws_vars.MicroState.axis_flags[eje_avance]['maq_est_val'] == initial_state,                      # eje avance ON
            ws_vars.MicroState.axis_flags[eje_carga]['drv_flags'] & msg_base.DrvFbkDataFlags.ENABLED == 0,  # eje carga OFF
            ws_vars.MicroState.axis_flags[eje_avance]['sync_on'] == 0,                                            # Sincronismo OFF
            round(ws_vars.MicroState.axis_measures[eje_avance]['pos_fil'], 0) == round(ctrl_vars.ROSCADO_CONSTANTES['posicion_de_inicio'], 0)   # Eje avance en posición de inicio
        ]
        print(init_flags)
        if False in init_flags:
            return False

        # Paso 1 - Acopla lubricante
        roscado_init_flags = [
            ws_vars.MicroState.rem_i_states[1]['clampeo_plato_expandido'],          # Plato clampeado
        ]

        if False in roscado_init_flags:
            self.err_msg.append('Error en condiciones de avanzar puntera en boquilla durante carga')
            return False
        
        pos = round(ws_vars.MicroState.axis_measures[ctrl_vars.AXIS_IDS['carga']]['pos_fil'], 0)
        if pos not in ctrl_vars.LOAD_STEPS:
            print('Error en posicion de cabezal')
            return False
        
        key = 'expandir_acople_lubric'
        wait_key = 'acople_lubric_expandido'
        group = 1
        wait_group = 1
        if not self.send_pneumatic(key, group, 1):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print("PASO 1")

        # Paso 2 - Encender bomba solube
        key = 'encender_bomba_soluble'
        group = 1
        if not self.send_pneumatic(key, group, 1):
            return False
        print("PASO 2")

        # Paso 3 - Presurizar ON
        ws_vars.MicroState.roscado_allow_presure_off = False
        key = 'presurizar'
        group = 1
        if not self.send_pneumatic(key, group, 1):
            return False
        print("PASO 3")

        # Paso 4 - Cerrar boquilla hidráulica
        boquilla = self.get_current_boquilla_roscado()
        key_1 = 'cerrar_boquilla_' + str(boquilla)
        key_2 = 'abrir_boquilla_' + str(boquilla)
        group = 1
        self.send_pneumatic(key_1, group, 1, key_2, 0)
        print("PASO 4")

        # Paso 5 - Avanzar a pos y vel de aproximacion
        axis = ctrl_vars.AXIS_IDS['avance']
        command = Commands.mov_to_pos
        msg_id = self.get_message_id()
        ref = ctrl_vars.ROSCADO_CONSTANTES['posicion_de_aproximacion']
        header, data = build_msg(
            command,
            ref = ref,
            ref_rate = ctrl_vars.ROSCADO_CONSTANTES['velocidad_en_vacio'],
            msg_id = msg_id,
            eje = axis)
        if not self.send_message(header, data):
            return False
        
        if not self.wait_for_lineal_mov(ref):
            return False
        print("PASO 5")

        # Paso 6 - Dejar boquilla en centro cerrado
        boquilla = self.get_current_boquilla_roscado()
        key_1 = 'cerrar_boquilla_' + str(boquilla)
        key_2 = 'abrir_boquilla_' + str(boquilla)
        group = 1
        self.send_pneumatic(key_1, group, 0, key_2, 0)
        time.sleep(0.5)
        print("PASO 6 - Dejar boquilla en centro cerrado")


        # Paso 7 - Sale de safe para encender el husillo
        command = Commands.power_on
        axis = ctrl_vars.AXIS_IDS['giro']
        msg_id = self.get_message_id()
        header = build_msg(command, eje=axis, msg_id=msg_id)
        if not self.send_message(header):
            return False
        
        target_state = msg_app.StateMachine.EST_INITIAL
        if not self.wait_for_axis_state(target_state, axis):
            return False
        print('PASO 7 - Sale de safe para encender el husillo')

        # Paso 8 - Sincronizado ON
        command = Commands.sync_on
        axis = ctrl_vars.AXIS_IDS['avance']
        paso = ctrl_vars.ROSCADO_CONSTANTES['paso_de_rosca']
        header, data = build_msg(command, eje=axis, msg_id=msg_id, paso=paso)
        if not self.send_message(header, data):
            return False
        print("SYNC ON SENT")
        state = ws_vars.MicroState.axis_flags[axis]['sync_on']
        while not state:
            state = ws_vars.MicroState.axis_flags[axis]['sync_on']
            time.sleep(self.wait_time)

        print("PASO 8 - SINC ON")


        # Paso 9 - Presurizar OFF
        load_id = ctrl_vars.ROUTINE_IDS['carga']
        load_running = RoutineInfo.objects.get(name=ctrl_vars.ROUTINE_NAMES[load_id]).running == 1
        
        if load_running:
            if self.wait_presure_off_allowed(load_id) == False:
                return False

        ws_vars.MicroState.roscado_allow_presure_off = True
        key = 'presurizar'
        group = 1
        self.send_pneumatic(key, group, 0)
        print('PASO 9 - PRESURIZAR OFF')


        # Paso 10 - Avanzar a pos y vel final de roscado
        axis = ctrl_vars.AXIS_IDS['avance']
        command = Commands.mov_to_pos
        msg_id = self.get_message_id()
        ref = ctrl_vars.ROSCADO_CONSTANTES['posicion_final_de_roscado']
        header, data = build_msg(
            command,
            ref = ref,
            ref_rate = ctrl_vars.ROSCADO_CONSTANTES['velocidad_de_roscado'],
            msg_id = msg_id,
            eje = axis)
        if not self.send_message(header, data):
            return False
        
        if not self.wait_for_lineal_mov(ref):
            return False

        print("PASO 10 - Avanzar a pos y vel final de roscado")

        # Paso 11 - Avanzar a pos y vel de salida de rosca
        axis = ctrl_vars.AXIS_IDS['avance']
        command = Commands.mov_to_pos
        msg_id = self.get_message_id()
        ref = ctrl_vars.ROSCADO_CONSTANTES['posicion_salida_de_roscado']
        header, data = build_msg(
            command,
            ref = ref,
            ref_rate = ctrl_vars.ROSCADO_CONSTANTES['velocidad_de_retraccion'],
            msg_id = msg_id,
            eje = axis)
        if not self.send_message(header, data):
            return False
        
        if not self.wait_for_lineal_mov(ref):
            return False
        print("Paso 11 - Avanzar a pos y vel de salida de rosca")

        # Paso 12 - Sincronizado OFF
        command = Commands.sync_off
        axis = ctrl_vars.AXIS_IDS['avance']
        header = build_msg(command, eje=axis, msg_id=msg_id, paso=paso)
        if not self.send_message(header):
            return False

        state = ws_vars.MicroState.axis_flags[axis]['sync_on']
        while state:
            state = ws_vars.MicroState.axis_flags[axis]['sync_on']
            time.sleep(self.wait_time)

        print('Paso 12 - Sincronizado OFF')

        # Paso 13 - Enable husillo OFF
        command = Commands.power_off
        axis = ctrl_vars.AXIS_IDS['giro']
        drv_flag = msg_base.DrvFbkDataFlags.ENABLED
        msg_id = self.get_message_id()
        header = build_msg(command, eje=axis, msg_id=msg_id)
        if not self.send_message(header):
            return False
        
        if not self.wait_for_drv_flag(drv_flag, axis, 0):
            return False
        print('Paso 13 - Enable husillo OFF')

        # Paso 14 - Avance a posicion de inicio
        axis = ctrl_vars.AXIS_IDS['avance']
        command = Commands.mov_to_pos
        msg_id = self.get_message_id()
        ref = ctrl_vars.ROSCADO_CONSTANTES['posicion_de_inicio']
        header, data = build_msg(
            command,
            ref = ref,
            ref_rate = ctrl_vars.ROSCADO_CONSTANTES['velocidad_en_vacio'],
            msg_id = msg_id,
            eje = axis)
        
        if not self.send_message(header, data):
            return False

        if not self.wait_for_lineal_mov(ref):
            return False
        print('Paso 14 - Avance a posicion de inicio')

        # Paso 15 - Apagar bomba solube
        key = 'encender_bomba_soluble'
        group = 1
        if not self.send_pneumatic(key, group, 0):
            return False
        print("Paso 15 - Apagar bomba solube")

        # Paso 16 - Desacopla lubricante
        key = 'expandir_acople_lubric'
        wait_key = 'acople_lubric_contraido'
        group = 1
        wait_group = 1
        if not self.send_pneumatic(key, group, 0):
            return False
        if not self.wait_for_remote_in_flag(wait_key, wait_group):
            return False
        print("Paso 16 - Desacopla lubricante")



        
        print("FIN RUTINA ROSCADO")
        return True


    def routine_homing(self):
        eje_avance = ctrl_vars.AXIS_IDS['avance']
        eje_carga = ctrl_vars.AXIS_IDS['carga']
        initial_state = msg_app.StateMachine.EST_INITIAL
        # Paso 0 - Chequear condiciones iniciales - Todos los valores deben ser True par que empiece la rutina
        init_flags = [
            ws_vars.MicroState.axis_flags[eje_avance]['maq_est_val'] == initial_state,  # eje avance ON
            ws_vars.MicroState.rem_i_states[1]['acople_lubric_contraido'],              # acople_lubricante_contraido
            ws_vars.MicroState.rem_i_states[0]['puntera_descarga_contraida'],           # puntera_descarga_contraida
            ws_vars.MicroState.rem_i_states[0]['puntera_carga_contraida']               # puntera_carga_contraida
        ]
        print(init_flags)
        if False in init_flags:
            return False

        # Paso 0.1 - Encender bomba hidráulica
        key = 'encender_bomba_hidraulica'
        group = 1
        if not self.send_pneumatic(key, group, 1):
            return False

        # Paso 1 - Cerado eje avance
        command = Commands.run_zeroing
        axis = ctrl_vars.AXIS_IDS['avance']
        msg_id = self.get_message_id()
        header = build_msg(command, msg_id=msg_id, eje=axis)
        if not self.send_message(header):
            return False

        state = ws_vars.MicroState.axis_flags[axis]['home_switch']
        while not state:
            state = ws_vars.MicroState.axis_flags[axis]['home_switch']
            print(state)
            time.sleep(self.wait_time)
        print('PASO 1')
        print('HOME SW ACTIVADO')

        # Paso 1.1 - Chequeo cero
        if not self.wait_for_lineal_mov(0):
            return False
        print('Paso 1.1 - Chequeo cero')

        # Paso 1.2 - Mover a posición de inicio
        pos_inicio = ctrl_vars.ROSCADO_CONSTANTES['posicion_de_inicio']
        if not self.mov_to_pos_lineal(pos_inicio):
            return False
        print('Mov to pos')
        if not self.wait_for_lineal_mov(pos_inicio):
            return False
        print('Paso 1.2 - Mover a posición de inicio')

        # Paso 2 - Liberar plato
        key_1 = 'contraer_clampeo_plato'
        key_2 = 'expandir_clampeo_plato'
        if not self.send_pneumatic(key_1, 1, 1, key_2, 0):
            return False
        
        if not self.wait_for_remote_in_flag('clampeo_plato_contraido', 1):
            return False
        print('PASO 2')

        # Paso 2.1 - Encender servo
        command = Commands.power_on
        axis = ctrl_vars.AXIS_IDS['carga']
        msg_id = self.get_message_id()
        header = build_msg(command, eje=axis, msg_id=msg_id)
        if not self.send_message(header):
            return False
        
        target_state = msg_app.StateMachine.EST_INITIAL
        if not self.wait_for_axis_state(target_state, axis):
            return False
        print('Paso 2.1 - Encender servo')

        # Paso 3 - Cerado eje carga
        print("CERAR EJE CARGA")
        command = Commands.run_zeroing
        axis = ctrl_vars.AXIS_IDS['carga']
        msg_id = self.get_message_id()
        header = build_msg(command, msg_id=msg_id, eje=axis)
        if not self.send_message(header):
            return False
        print('PASO 3')

        # Paso 4 - Esperar sensor homing activado
        state = ws_vars.MicroState.axis_flags[axis]['home_switch']
        while not state:
            state = ws_vars.MicroState.axis_flags[axis]['home_switch']
            # print(state)
            time.sleep(0.01)
        print('HOME SW ACTIVADO')
        # Espera a que salga de la chapa
        while state:
            state = ws_vars.MicroState.axis_flags[axis]['home_switch']
            time.sleep(0.01)
        print('HOME SW DESACTIVADO')
        # Esperar fin de secuencia de homing
        time.sleep(1)
        current_pos = round(ws_vars.MicroState.axis_measures[axis]['pos_abs'], 2)
        prev_pos = -1.0
        while current_pos != prev_pos:
            print(current_pos, prev_pos)
            prev_pos = current_pos
            time.sleep(self.wait_time*3)
            current_pos = round(ws_vars.MicroState.axis_measures[axis]['pos_abs'], 2)
        print(current_pos)
        print("FIN COMANDO HOMING")
        time.sleep(2)
        # gira una posición buscando la chapa
        command = Commands.mov_to_pos
        msg_id = self.get_message_id()
        header, data = build_msg(command, ref=45, ref_rate=5, msg_id=msg_id, eje=axis)
        if not self.send_message(header, data):
            return False
        print('gira una posición buscando la chapa')
        # Espera sensor home activado
        state = ws_vars.MicroState.axis_flags[axis]['home_switch']
        while not state:
            state = ws_vars.MicroState.axis_flags[axis]['home_switch']
            time.sleep(self.wait_time)
        pos = ws_vars.MicroState.axis_measures[axis]['pos_fil']
        print('Espera sensor home activado')
        print("POSICION EN CHAPA", pos)
        # Detener eje
        command = Commands.stop
        msg_id = self.get_message_id()
        header = build_msg(command, msg_id=msg_id, eje=axis)
        if not self.send_message(header):
            return False
        time.sleep(0.5)
        print('Detener eje')
        # Configura cero
        header = None
        data = None
        if pos > ctrl_vars.HOMING_CONSTANTES['position_positive_7']:
            print('Caso 1, p0=7.2')
            command = Commands.drv_set_zero_abs
            msg_id = self.get_message_id()
            header, data = build_msg(command, msg_id=msg_id, zero=7.2, eje=axis)
        elif pos >= ctrl_vars.HOMING_CONSTANTES['position_mid_low'] and pos <= ctrl_vars.HOMING_CONSTANTES['position_mid_high']:
            print('Caso 2, p0=0')
        elif pos < ctrl_vars.HOMING_CONSTANTES['position_negative_7']:
            print('Caso 3, p0=-7.2')
            command = Commands.drv_set_zero_abs
            msg_id = self.get_message_id()
            header, data = build_msg(command, msg_id=msg_id, zero=-7.2, eje=axis)
        if header:
            print("SENDING P0")
            print(data, data.zero)
            if not self.send_message(header, data):
                return False
        time.sleep(2)
        command = Commands.mov_to_pos
        msg_id = self.get_message_id()
        header, data = build_msg(command, ref=0, ref_rate=40, msg_id=msg_id, eje=axis)
        if not self.send_message(header, data):
            return False
        print('Configura cero')
        print('PASO 4')

        # Paso 5 - Clampea plato
        key_1 = 'expandir_clampeo_plato'
        key_2 = 'contraer_clampeo_plato'
        group = 1
        if not self.send_pneumatic(key_1, group, 1, key_2, 0):
            return False
        
        if not self.wait_for_remote_in_flag('clampeo_plato_expandido', group):
            return False
        print('PASO 5 - Clampea plato')

        # Paso 6 - Power off
        command = Commands.power_off
        drv_flag = msg_base.DrvFbkDataFlags.ENABLED
        axis = ctrl_vars.AXIS_IDS['carga']
        msg_id = self.get_message_id()
        header = build_msg(command, eje=axis, msg_id=msg_id)
        if not self.send_message(header):
            return False
        
        if not self.wait_for_drv_flag(drv_flag, axis, 0):
            return False
        print('PASO 6 - Power off')

        print('FIN RUTINA HOMING')
        return True
       

    def send_message(self, header, data=None):
        if self.ch_info:
            if data:
                send_message(header, self.ch_info, data)
            else:
                send_message(header, self.ch_info)
            return True
        print('send msg false')
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
        timer = 0
        stop_flags_ok = self.check_stop_flags(timeout=ctrl_vars.TIMEOUT_PNEUMATIC)
        while not flag and stop_flags_ok:     # Verifica que el flag está en HIGH
            flag = ws_vars.MicroState.rem_i_states[group][flag_key]
            time.sleep(self.wait_time)
            stop_flags_ok = self.check_stop_flags(timer=timer, timeout=ctrl_vars.TIMEOUT_PNEUMATIC)
            timer += self.wait_time
        if not flag:
            return False
        return True


    def wait_for_not_remote_in_flag(self, flag_key, group):
        flag = ws_vars.MicroState.rem_i_states[group][flag_key]
        timer = 0
        stop_flags_ok = self.check_stop_flags(timeout=ctrl_vars.TIMEOUT_PNEUMATIC)
        while flag and stop_flags_ok:     # Verifica que el flag está en LOW
            flag = ws_vars.MicroState.rem_i_states[group][flag_key]
            time.sleep(self.wait_time)
            timer += self.wait_time
            stop_flags_ok = self.check_stop_flags(timer=timer, timeout=ctrl_vars.TIMEOUT_PNEUMATIC)
        if flag:
            return False
        return True


    def wait_for_axis_state(self, target_state, axis):
        current_state_value = ws_vars.MicroState.axis_flags[axis]['maq_est_val']
        timer = 0
        timeout = ctrl_vars.TIMEOUT_STATE_CHANGE
        err_msg='cambio de estado de eje'
        stop_flags_ok = self.check_stop_flags(err_msg=err_msg, timeout=timeout, axis=axis)
        
        while current_state_value != target_state and stop_flags_ok:
            current_state_value = ws_vars.MicroState.axis_flags[axis]['maq_est_val']
            time.sleep(self.wait_time)
            timer += self.wait_time
            stop_flags_ok = self.check_stop_flags(err_msg=err_msg, timer=timer, timeout=timeout, axis=axis)
        print('Estado eje:', current_state_value)
        if stop_flags_ok == False:
            return False

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
        timer = 0
        stop_flags_ok = self.check_stop_flags(err_msg='indexado', timeout=ctrl_vars.TIMEOUT_LOAD, axis=axis)
        while not (pos >= nex_step - 1 and pos <= nex_step + 1) and stop_flags_ok:
            pos = ws_vars.MicroState.axis_measures[axis]['pos_fil']
            time.sleep(self.wait_time)
            timer += self.wait_time
            stop_flags_ok = self.check_stop_flags(err_msg='indexado', timer=timer, timeout=ctrl_vars.TIMEOUT_LOAD, axis=axis)

        if stop_flags_ok == False:
            return False

        return self.wait_for_axis_state(msg_app.StateMachine.EST_INITIAL, axis)


    def wait_for_lineal_mov(self, target_pos):
        axis = ctrl_vars.AXIS_IDS['avance']
        current_pos = ws_vars.MicroState.axis_measures[axis]['pos_fil']
        timer = 0
        stop_flags_ok = self.check_stop_flags(err_msg='movimiento lineal', timeout=ctrl_vars.TIMEOUT_LINEAL, axis=axis)
        
        while not (current_pos >= target_pos - 0.1 and current_pos <= target_pos + 0.1) and stop_flags_ok:
            current_pos = ws_vars.MicroState.axis_measures[axis]['pos_fil']
            time.sleep(self.wait_time)
            timer += self.wait_time
            stop_flags_ok = self.check_stop_flags(err_msg='movimiento lineal', timeout=ctrl_vars.TIMEOUT_LINEAL, axis=axis)

        if stop_flags_ok == False:
            return False
        
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
        if current_step >= 0:
            return ctrl_vars.BOQUILLA_DESCARGADOR[current_step]
        return False


    def get_current_boquilla_roscado(self):
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
        if current_step >= 0:
            return ctrl_vars.BOQUILLA_ROSCADO[current_step]
        return False


    def mov_to_pos_lineal(self, target_pos, ref_rate=ctrl_vars.ROSCADO_CONSTANTES['velocidad_en_vacio']):   # Sends cmd to move to target position on lineal axis
        axis = ctrl_vars.AXIS_IDS['avance']
        command = Commands.mov_to_pos
        msg_id = self.get_message_id()
        ref = target_pos
        header, data = build_msg(
            command,
            ref = ref,
            ref_rate = ref_rate,
            msg_id = msg_id,
            eje = axis)
        print('sending mov to pos lineal cmd')
        if not self.send_message(header, data):
            print('send false')
            return False
        print('send true')
        return True


    def stop(self):
        self._stop_event.set()

    def wait_for_drv_flag(self, flag, axis, flag_value):
        drv_flags = ws_vars.MicroState.axis_flags[axis]['drv_flags']
        timer = 0
        stop_flags_ok = self.check_stop_flags(timeout=ctrl_vars.TIMEOUT_STATE_CHANGE)
        while drv_flags & flag != flag_value and stop_flags_ok == True:
            drv_flags = ws_vars.MicroState.axis_flags[axis]['drv_flags']
            time.sleep(self.wait_time)
            stop_flags_ok = self.check_stop_flags(timer=timer, timeout=ctrl_vars.TIMEOUT_STATE_CHANGE)
        if drv_flags & flag != flag_value:
            return False
        return True


    def check_stop_flags(self, err_msg='', timer=0, timeout=ctrl_vars.TIMEOUT_GENERAL, axis=None):
        msg = ''

        if timer >= timeout:
            msg = 'Timeout'
            if err_msg:
                msg += ' en ' + err_msg
            self.err_msg.append(msg)
            return False

        if axis or axis == 0:
            if ws_vars.MicroState.axis_flags[axis]['em_stop']:
                msg = 'Parada de emergencia (eje)'
                if err_msg:
                    msg += ' en ' + err_msg
                self.err_msg.append(msg)
                return False
        
        if ws_vars.MicroState.micro_flags['em_stop'] == True:
            msg = 'Parada de emergencia (general)'
            if err_msg:
                msg += ' en ' + err_msg
            self.err_msg.append(msg)
            return False
        
        if ws_vars.MicroState.routine_stopped == True:
            msg = 'Rutina detenida'
            if err_msg:
                msg += ' en ' + err_msg
            self.err_msg.append(msg)
            return False

        return True


    def check_running_routines(self):
        for routine in RoutineInfo.objects.all():
            if routine.running == 1:
                return True
        return False


    def set_routine_ongoing_flag(self):
        if self.check_running_routines():
            ws_vars.MicroState.routine_ongoing = True
        else:
            ws_vars.MicroState.routine_ongoing = False

    
    def wait_presure_off_allowed(self, routine):
        stop_flags_ok = self.check_stop_flags()
        load_id = ctrl_vars.ROUTINE_IDS['carga']
        
        if routine == load_id:
            flag = ws_vars.MicroState.load_allow_presure_off
        else:
            flag = ws_vars.MicroState.roscado_allow_presure_off
        
        while flag == False and stop_flags_ok == True:
            time.sleep(self.wait_time)
            stop_flags_ok = self.check_stop_flags()
            if routine == load_id:
                flag = ws_vars.MicroState.load_allow_presure_off
            else:
                flag = ws_vars.MicroState.roscado_allow_presure_off
        
        if stop_flags_ok == False:
            return False

        return True
        


    def stopped(self):
        return self._stop_event.it_set()



class MasterHandler(threading.Thread):

    def __init__(self, **kwargs):
        super(MasterHandler, self).__init__(**kwargs)
        self.wait_time = 0.2
        self.wait_rtn_time = 0.5
        self.timer = 0
        self.init_rtn_timeout = 20
    

    def run(self):
        ws_vars.MicroState.master_running = True
        ws_vars.MicroState.master_stop = False
        ws_vars.MicroState.iteration = 0
        roscado_id = ctrl_vars.ROUTINE_IDS['roscado']
        carga_id = ctrl_vars.ROUTINE_IDS['carga']
        descarga_id = ctrl_vars.ROUTINE_IDS['descarga']
        indexar_id = ctrl_vars.ROUTINE_IDS['cabezal_indexar']

        while ws_vars.MicroState.master_stop == False:
            running_ids = self.get_running_routines()
            print('\nRUNNING RTNS', running_ids)
            if carga_id not in running_ids:
                print('RUTINA CARGA')
                RoutineHandler(carga_id).start()
                
                if self.wait_init_rtn(carga_id) == False:
                    return

            if ws_vars.MicroState.iteration >= 1:
                if roscado_id not in running_ids:
                    print('RUTINA ROSCADO')
                    RoutineHandler(roscado_id).start()
                
                    if self.wait_init_rtn(roscado_id) == False:
                        return
            
            if ws_vars.MicroState.iteration >= 2:
                if descarga_id not in running_ids:
                    print('RUTINA DESCARGA')
                    RoutineHandler(descarga_id).start()

                    if self.wait_init_rtn(descarga_id) == False:
                        return

            while ws_vars.MicroState.routine_ongoing == True and ws_vars.MicroState.master_stop == False:
                time.sleep(self.wait_rtn_time)
            
            if ws_vars.MicroState.master_stop:
                ws_vars.MicroState.master_running = False
                return
            
            running_ids = self.get_running_routines()
            if indexar_id not in running_ids:
                print('RUTINA INDEXAR')
                RoutineHandler(indexar_id).start()

                if self.wait_init_rtn(indexar_id) == False:
                    return
            
            while indexar_id in running_ids and ws_vars.MicroState.master_stop == False:
                time.sleep(self.wait_rtn_time)
                running_ids = self.get_running_routines()
            
            if ws_vars.MicroState.master_stop == True:
                ws_vars.MicroState.master_running = False
                return

            if ws_vars.MicroState.iteration < 2:
                ws_vars.MicroState.iteration += 1
            
            if ws_vars.MicroState.master_stop == True:
                ws_vars.MicroState.master_running = False
                return
        return
        
    def get_running_routines(self):
        running_routines = []
        for routine in RoutineInfo.objects.all():
            if routine.running == 1:
                running_routines.append(ctrl_vars.ROUTINE_IDS[routine.name])
        return running_routines
    
    def check_timeout_exceeded(self, timeout):
        if self.timer >= timeout or ws_vars.MicroState.master_stop == True:
            ws_vars.MicroState.master_running = False
            return True
        return False
    
    def wait_init_rtn(self, routine_id):
        running_ids = self.get_running_routines()
        timeout_exceeded = self.check_timeout_exceeded(self.init_rtn_timeout)

        while routine_id not in running_ids and timeout_exceeded == False:
            time.sleep(self.wait_time)
            self.timer += self.wait_time
            running_ids = self.get_running_routines()
            timeout_exceeded = self.check_timeout_exceeded(self.init_rtn_timeout)
        
        if timeout_exceeded:
            print('Timeout esperando inicio de rutina', routine_id)
            ws_vars.MicroState.master_stop = True
            ws_vars.MicroState.master_running = False
            return False
        self.timer = 0
        return True