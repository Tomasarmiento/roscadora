# coding=utf-8
import struct, ctypes
from ctypes import c_int, c_long, c_uint16, c_uint32, c_float, c_bool, c_ulong

from .messages_base import AcdpAvi, AcdpMsgType, AcdpMsgLevel, AcdpPiT0Config, AcdpPiT0Data,\
    AcdpPidT1Config, AcdpPidT1Data, BaseStructure, BaseUnion, AcdpDrvFbkData, AcdpEncData,\
        AcdpDrvCmdData, AcdpAviData

# --------------------------------------------------------------------------------------------#
# --------------------- Códigos de Mensajes propios de la aplicación -------------------------#
# --------------------------------------------------------------------------------------------#

class AcdpMsgCodes:
    
    class CfgSet:       # Seteo configuracion
        CD_MOV_POS = AcdpMsgType.CFG_SET + AcdpMsgLevel.APPLICATION + 0x01
        CD_MOV_FZA = AcdpMsgType.CFG_SET + AcdpMsgLevel.APPLICATION + 0x02
    
    class CfgReq:       # Solicitud configuracion
        CD_MOV_POS = AcdpMsgType.CFG_REQ + AcdpMsgLevel.APPLICATION + 0x01
        CD_MOV_FZA = AcdpMsgType.CFG_REQ + AcdpMsgLevel.APPLICATION + 0x02
    
    class CfgDat:       # Datos de configuracion
        CD_MOV_POS = AcdpMsgType.CFG_DAT + AcdpMsgLevel.APPLICATION + 0x01
        CD_MOV_FZA = AcdpMsgType.CFG_DAT + AcdpMsgLevel.APPLICATION + 0x02
    
    class Cmd:          # Comandos
        Cd_MovEje_Stop               = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x01
        Cd_MovEje_FastStop           = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x02
        Cd_MovEje_PowerOn            = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x03
        Cd_MovEje_PowerOff           = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x04
        Cd_MovEje_SyncOn             = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x05  # Parametro: Param::tSyncOn
        Cd_MovEje_SyncOff            = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x06
        Cd_MovEje_RunZeroing         = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x07
        Cd_MovEje_RunPositioning     = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x08
        Cd_MovEje_MovToVel           = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x09  # Parametro: Param::tMovToVel
        Cd_MovEje_SetRefVel          = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x0a  # Parametro: Param::tSetRefVel
        Cd_MovEje_MovToPos           = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x0b  # Parametro: Param::tMovToPos
        Cd_MovEje_SetRefPos          = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x0c  # Parametro: Param::tSetRefPos
        Cd_MovEje_MovToPos_Yield     = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x0d  # Parametro: Param::tMovToPos_Yield
        Cd_MovEje_MovToPosLoad       = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x0e  # Parametro: Param::tMovToPosLoad
        Cd_MovEje_SetRefPosLoad      = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x0f  # Parametro: Param::tSetRefPosLoad
        Cd_MovEje_MovToPosLoad_Yield = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x10  # Parametro: Param::tMovToPosLoad_Yield
        Cd_MovEje_MovToFza           = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x11  # Parametro: Param::tMovToFza
        Cd_MovEje_SetRefFza          = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x12  # Parametro: Param::tSetRefFza
        Cd_MovEje_MovToFza_Yield     = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x13  # Parametro: Param::tMovToFza_Yield

        Cd_BalizaEnsayo_ApagarCancelado    = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x21
        Cd_BalizaEnsayo_EncenderCancelado  = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x22
        Cd_BalizaEnsayo_ApagarNoPasa       = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x23
        Cd_BalizaEnsayo_EncenderNoPasa     = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x24
        Cd_BalizaEnsayo_ApagarPasa         = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x25
        Cd_BalizaEnsayo_EncenderPasa       = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x26
        Cd_BalizaEnsayo_ApagarEnsayando    = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x27
        Cd_BalizaEnsayo_EncenderEnsayando  = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x28


# --------------------------------------------------------------------------------------------#
# ------------------------------ Parametros de los comandos ----------------------------------#
# --------------------------------------------------------------------------------------------#


class AcdpMsgParamsSyncOn(BaseStructure):
    _fields_ = [
        ('paso_eje_lineal', c_float)
    ]


class AcdpMsgParamsYield(BaseStructure):
    _fields_ = [
        ('factor_limite_elastico', c_float),
        ('correccion_pendiente', c_float),
        ('cedencia', c_float)
    ]


class AcdpMsgParamsMovToVel(BaseStructure):
    _fields_ = [
        ('reference', c_float)
    ]


class AcdpMsgParamsSetRefVel(BaseStructure):
    _fields_ = [
        ('reference', c_float)
    ]


class AcdpMsgParamsMovToPos(BaseStructure):
    _fields_ = [
        ('reference', c_float),
        ('ref_rate', c_float)
    ]


class AcdpMsgParamsSetRefPos(BaseStructure):
    _fields_ = [
        ('reference', c_float)
    ]


class AcdpMsgParamsMovToPosYield(BaseStructure):
    _fields_ = [
        ('mov_to_pos', AcdpMsgParamsMovToPos),
        ('yield', AcdpMsgParamsYield)
    ]


class AcdpMsgParamsMovToPosLoad(BaseStructure):
    _fields_ = [
        ('reference', c_float),
        ('ref_rate', c_float)
    ]


class AcdpMsgParamsSetRefPosLoad(BaseStructure):
    _fields_ = [
        ('reference', c_float)
    ]


class AcdpMsgParamsMovToPosLoadYield(BaseStructure):
    _fields_ = [
        ('mov_to_pos_load', AcdpMsgParamsMovToPosLoad),
        ('yield', AcdpMsgParamsYield)
    ]


class AcdpMsgParamsMovToFza(BaseStructure):
    _fields_ = [
        ('reference', c_float),
        ('ref_rate', c_float),
        ('vel_uns_max', c_float)
    ]


class AcdpMsgParamsSetRefFza(BaseStructure):
    _fields_ = [
        ('reference', c_float)
    ]


class AcdpMsgParamsMovToFzaYield(BaseStructure):
    _fields_ = [
        ('mov_to_fza', AcdpMsgParamsMovToFza),
        ('yield', AcdpMsgParamsYield)
    ]


class AcdpMsgParams(BaseStructure):
    _fields_ = [
        
        # Sincronismo
        # ------------------------------------------------
        ('sync_on', AcdpMsgParamsSyncOn),

        # Movimientos
        # ------------------------------------------------
        ('yield', AcdpMsgParamsYield),

        # Movimiento en velocidad
        # ------------------------------------------------
        ('mov_to_vel', AcdpMsgParamsMovToVel),
        ('set_ref_vel', AcdpMsgParamsSetRefVel),

        # Movimiento en posicion
        # ------------------------------------------------
        ('mov_to_pos', AcdpMsgParamsMovToPos),
        ('set_ref_pos', AcdpMsgParamsSetRefPos),
        ('mov_to_pos_yield', AcdpMsgParamsMovToPosYield),

        # Movimiento en posicion vista en la carga
        # ------------------------------------------------
        ('mov_to_pos_load', AcdpMsgParamsMovToPosLoad),
        ('set_ref_pos_load', AcdpMsgParamsSetRefPosLoad),
        ('mov_to_pos_load_yield', AcdpMsgParamsMovToPosLoadYield),

        # Movimiento en fuerza
        # ------------------------------------------------
        ('mov_to_fza', AcdpMsgParamsMovToFza),
        ('set_ref_fza', AcdpMsgParamsSetRefFza),
        ('mov_to_fza_yield', AcdpMsgParamsMovToFzaYield)
    ]


###############################################################################################
##################################### Estructuras #############################################
###############################################################################################


# --------------------------------------------------------------------------------------------#
# ------------------------------------- Control ----------------------------------------------#
# --------------------------------------------------------------------------------------------#

class AcdpControlEnums:
    # Analog inputs
    ID_X_AVI_FZA            = 0
    CANT_AVI                = 1

    # Encoders
    ID_X_ENC_RESERV_1       = 0
    ID_X_ENC_LOAD           = 1
    CANT_ENC                = 2

    # Drivers - Ethercat
    ID_X_DRV_ECAT_AVANCE    = 0
    ID_X_DRV_ECAT_GIRO      = 1
    ID_X_DRV_ECAT_CARGA     = 2
    CANT_DRV_ECAT           = 3

    # Drivers - Analog Reference
    ID_X_DRV_ANA_RESERV_1   = 0
    ID_X_DRV_ANA_RESERV_2   = 1
    CANT_DRV_ANA            = 2

    # Drivers - Pulse Reference
    ID_X_DRV_PULSE_RESERV_1 = 0
    CANT_DRV_PULSE          = 1


# --------------------------------------------------------------------------------------------#
# --------------------------------- Movimientos Eje ------------------------------------------#
# --------------------------------------------------------------------------------------------#


class AcdpAxisMovementEnums:
    ID_X_EJE_FIRSTROSCADO   = 0
    ID_X_EJE_PREV_ROSCADO   = ID_X_EJE_FIRSTROSCADO - 1
    ID_X_EJE_GIRO           = ID_X_EJE_PREV_ROSCADO + 1
    ID_X_EJE_AVANCE         = ID_X_EJE_GIRO + 1
    ID_X_EJE_POST_ROSCADO   = ID_X_EJE_AVANCE + 1
    ID_X_EJE_LAST_ROSCADO   = ID_X_EJE_POST_ROSCADO - 1

    ID_X_EJE_FIRST_CARGA    = ID_X_EJE_LAST_ROSCADO + 1
    ID_X_EJE_PREV_CARGA     = ID_X_EJE_FIRST_CARGA - 1
    ID_X_EJE_CARGA          = ID_X_EJE_PREV_CARGA + 1
    ID_X_EJE_POST_CARGA     = ID_X_EJE_CARGA + 1
    ID_X_EJE_LAST_CARGA     = ID_X_EJE_POST_CARGA - 1

    CANT_EJES               = ID_X_EJE_LAST_CARGA + 1


class AcdpAxisMovementsMovPosConfigFlagsBits(BaseStructure):
    _fields_ = [
        ('limit_pos_enab', c_bool),
        ('homing_sw_positive', c_bool),
        ('homing_with_index', c_bool)
    ]


class AcdpAxisMovementsMovPosConfigFlags(BaseUnion):
    _fields_ = [
        ('all', c_ulong),
        ('bits', AcdpAxisMovementsMovPosConfigFlagsBits)
    ]


class AcdpAxisMovementsMovPosConfigHoming(BaseStructure):
    _fields_ = [
        ('vel_posic', c_float),
        ('vel_cerado', c_float)
    ]


class AcdpAxisMovementsMovPosConfigLimites(BaseStructure):
    _fields_ = [
        ('pos_min', c_float),
        ('pos_max', c_float)
    ]


class AcdpAxisMovementsMovPosConfigMed(BaseStructure):
    _fields_ = [
        ('tau_filtro_pos_drv', c_float),
        ('tau_filtro_pos_load', c_float)
    ]


class AcdpAxisMovementsMovPosConfig(BaseStructure):
    _fields_ = [
        ('flags', AcdpAxisMovementsMovPosConfigFlags),
        ('homing', AcdpAxisMovementsMovPosConfigHoming),
        ('limites', AcdpAxisMovementsMovPosConfigLimites),
        ('med', AcdpAxisMovementsMovPosConfigMed),

        ('ctrl_vel', AcdpPiT0Config),
        ('fast_stpo_decel', c_float),       # Cero desactiva el límite

        ('ctrl_pos', AcdpPidT1Config)
    ]


class AcdpAxisMovementsMovPosDataFlagsBits(BaseStructure):
    _fields_ = [
        ('zero_switch_on', c_bool),
        ('pos_min_switch_on', c_bool),
        ('pos_max_switch_on', c_bool),
        ('pos_min_limit', c_bool),
        ('pos_max_limit', c_bool),
        ('vel_limit', c_bool)
    ]


class AcdpAxisMovementsMovPosDataFlags(BaseUnion):
    _fields_ = [
        ('all', c_ulong),
        ('bits', AcdpAxisMovementsMovPosDataFlagsBits)
    ]


class AcdpAxisMovementsMovPosDataHoming(BaseStructure):
    _fields_ = [
        # Maquina de Estados Secuencia de cerado. Estados en AcdpAxisMovementsMovPosDataHomingStates
        ('estado', c_long)
    ]


class AcdpAxisMovementsMovPosDataHomingStates:
    EST_INICIAL             = 0
    EST_ACTIVACION_SWITCH   = 1
    EST_CAMBIO_DIRECCION    = 2
    EST_LIBERACION_SWITCH   = 3
    EST_INDEX_DETECTION     = 4


class AcdpAxisMovementsMovPosDataMedDrv(BaseStructure):
    _fields_ = [
        ('drv_fbk', AcdpDrvFbkData),
        ('pos_fil', c_float),
        ('vel_fil', c_float)
    ]


class AcdpAxisMovementsMovPosDataMedLoad(BaseStructure):
    _fields_ = [
        ('enc', AcdpEncData),
        ('pos_fil', c_float),
        ('vel_fil', c_float)
    ]


class AcdpAxisMovementsMovPosData(BaseStructure):
    _fields_ = [
        ('flags', AcdpAxisMovementsMovPosDataFlags),
        ('homing', AcdpAxisMovementsMovPosDataHoming),
        ('med_drv', AcdpAxisMovementsMovPosDataMedDrv),
        ('med_load', AcdpAxisMovementsMovPosDataMedLoad),

        ('ctrl_vel', AcdpPiT0Data),
        ('ctrl_pos', AcdpPidT1Data)
    ]


class AcdpAxisMovementsMovPos(BaseStructure):
    _fields_ = [
        # Config MovPos
        ('config', AcdpAxisMovementsMovPosConfig),

        # Data MovPos
        ('data', AcdpAxisMovementsMovPosData)
    ]


class AcdpAxisMovementsMovFzaConfigFlagsBits(BaseStructure):
    _fields_ = [
        ('limit_pos_enab', c_bool),
        ('rel_fza_pos_fija', c_bool),
        ('rel_fza_pos_negativa', c_bool)
    ]


class AcdpAxisMovementsMovFzaConfigFlags(BaseUnion):
    _fields_ = [
        ('all', c_ulong),
        ('bits', AcdpAxisMovementsMovFzaConfigFlagsBits)
    ]


class AcdpAxisMovementsMovFzaConfigLimites(BaseStructure):
    _fields_ = [
        ('fza_min', c_float),
        ('fza_max', c_float)
    ]


class AcdpAxisMovementsMovFzaConfigMedCalcRigidez(BaseStructure):
    _fields_ = [
        ('delta_pos', c_float)  # //[mm] Delta de posicion para el calculo de la rigidez
    ]


class AcdpAxisMovementsMovFzaConfigMed(BaseStructure):
    _fields_ = [
        ('tau_filtro_fza', c_float),    # [s] - Tau para el filtrado de las mediciones
        ('calc_rigidez', AcdpAxisMovementsMovFzaConfigMedCalcRigidez)
    ]


class AcdpAxisMovementsMovFzaConfigYield(BaseStructure):
    _fields_ = [
        ('fza_uns_min', c_float)    # [kgf] Fuerza minima utilizada para comenzar a evaluar el limite elastico
    ]


class AcdpAxisMovementsMovFzaConfig(BaseStructure):
    _fields_ = [
        ('flags', AcdpAxisMovementsMovFzaConfigFlags),
        ('limites', AcdpAxisMovementsMovFzaConfigLimites),
        ('med', AcdpAxisMovementsMovFzaConfigMed),
        ('yield', AcdpAxisMovementsMovFzaConfigYield),
        ('ctrl_fza', AcdpPidT1Config),
        ('rel_fza_pos_uns', c_float)    # [kgf/mm] Se usa para convertir la salida del control en velocidad
    ]


class AcdpAxisMovementsMovFzaDataFlagsBits(BaseStructure):
    _fields_ = [
        ('fza_min_limit', c_bool),  # 0
        ('fza_max_limit', c_bool),  # 1
        ('cedencia', c_bool)        # 2
    ]


class AcdpAxisMovementsMovFzaDataFlags(BaseUnion):
    _fields_ = [
        ('all', c_ulong),
        ('bits', AcdpAxisMovementsMovFzaDataFlagsBits)
    ]


class AcdpAxisMovementsMovFzaDataMed(BaseStructure):
    _fields_ = [
        ('cel', AcdpAviData),
        ('fza_fil', c_float),   # [kgf]

        ('rigidez_drive', c_float),     # [kgf/mm]
        ('rigidez_load', c_float),      # [kgf/mm]
        ('cedencia', c_float)           # [mm]
    ]


class AcdpAxisMovementsMovFzaData(BaseStructure):
    _fields_ = [
        ('flags', AcdpAxisMovementsMovFzaDataFlags),
        ('med', AcdpAxisMovementsMovFzaDataMed),
        ('ctrl_fza', AcdpPidT1Data),
        ('rel_fza_pos_uns', c_float)    # [kgf/mm]
    ]


class AcdpAxisMovementsMovFza(BaseStructure):
    _fields_ = [
        # Config MovFza
        ('config', AcdpAxisMovementsMovFzaConfig),

        # Data MovFza
        ('data', AcdpAxisMovementsMovFzaData)
    ]


class AcdpAxisMovementsMovEjeConfig(BaseStructure):
    _fields_ = [
        ('mov_pos', AcdpAxisMovementsMovPosConfig),
        ('mov_fza', AcdpAxisMovementsMovFzaConfig)
    ]


class AcdpAxisMovementsMovEjeDataFlagsBits(BaseStructure):
    _fields_ = [
        ('em_stop', c_bool),    # 0
        ('disabled', c_bool),   # 1
        ('sync_on', c_bool)     # 2
    ]


class AcdpAxisMovementsMovEjeDataFlags(BaseUnion):
    _fields_ = [
        ('all', c_ulong),
        ('flags', AcdpAxisMovementsMovEjeDataFlagsBits)
    ]


class AcdpAxisMovementsMovEjeDataMaqEst(BaseStructure):
    _fields_ = [
        ('flags_fin', c_ulong),    # Flags FinEstado. Ver AcdpAxisMovementsMovEjeDataMaqEstFlagsFin
        ('estado', c_long)        # Maquina de Estados General. Ver AcdpAxisMovementsMovEjeDataMaqEstEstado
    ]


class AcdpAxisMovementsMovEjeDataMaqEstFlagsFin:
    FLGFIN_OK                   = 1 << 0
    FLGFIN_CANCELED             = 1 << 1
    FLGFIN_EM_STOP              = 1 << 2
    FLGFIN_DRV_HOMING_ERROR     = 1 << 3
    FLGFIN_ECHO_TIMEOUT         = 1 << 4
    FLGFIN_POS_ABS_DISABLED     = 1 << 5
    FLGFIN_UNKNOWN_ZERO         = 1 << 6
    FLGFIN_POSFEED_BACK_ERROR   = 1 << 7
    FLGFIN_LIMIT_VEL_EXCEEDED   = 1 << 8
    FLGFIN_LIMIT_POS_EXCEEDED   = 1 << 9
    FLGFIN_LIMIT_FZA_EXCEEDED   = 1 << 10
    FLGFIN_YIELD                = 1 << 11
    FLGFIN_INVALID_STATE        = 1 << 12
    FLGFIN_DRV_NOT_ENABLED      = 1 << 13
    FLGFIN_AXIS_DISABLED        = 1 << 14


class AcdpAxisMovementsMovEjeDataMaqEstEstado:
    EST_SAFE                = 0
    EST_PRE_INITIAL         = 1
    EST_INITIAL             = 2
    EST_POWERING_ON         = 3
    EST_POWERING_OFF        = 4
    EST_STOPPING            = 5
    EST_FAST_STOPPING       = 6
    EST_HOMING              = 7
    EST_POSITIONING         = 8
    EST_MOV_TO_VEL          = 9
    EST_MOV_TO_POS          = 10
    EST_MOV_TO_POS_LOAD     = 11
    EST_MOV_TO_FZA          = 12


class AcdpAxisMovementsMovEjeDataSincroMedDrv(BaseStructure):
    _fields_ = [
        ('modulo', c_float),
        ('pos_dif', c_float),
        ('vel_dif', c_float)
    ]


class AcdpAxisMovementsMovEjeDataSincro(BaseStructure):
    _fields_ = [
        ('rel_master', c_float),
        ('set_point_dif', c_float),

        ('med_drv', AcdpAxisMovementsMovEjeDataSincroMedDrv)
    ]


class AcdpAxisMovementsMovEjeData(BaseStructure):
    _fields_ = [
        ('flags', AcdpAxisMovementsMovEjeDataFlags),
        ('maq_est', AcdpAxisMovementsMovEjeDataMaqEst),

        ('mov_pos', AcdpAxisMovementsMovPosData),
        ('sincro', AcdpAxisMovementsMovEjeDataSincro),  # Informacion sincronismo
        ('mov_fza', AcdpAxisMovementsMovFzaData),

        ('drive', AcdpDrvCmdData)
    ]


class AcdpAxisMovementsMovEje(BaseStructure):
    _fields_ = [
        # Configuracion Movimiento Eje
        ('config', AcdpAxisMovementsMovEjeConfig),

        # Datos Movimiento Eje
        ('data', AcdpAxisMovementsMovEjeData)
    ]


class AcdpAxisMovements(BaseStructure):
    _fields_ = [
        # Movimiento Posicion
        ('mov_pos', AcdpAxisMovementsMovPos),

        # Movimiento Fuerza
        ('mov_fza', AcdpAxisMovementsMovFza),

        # Movimiento Eje
        ('mov_eje', AcdpAxisMovementsMovEje)
    ]


class AcdpPcDataFlagsBits(BaseStructure):
    _fields_ = [
        ('cmd_toggle', c_bool),     # 0
        ('cmd_received', c_bool)    # 1
    ]


class AcdpPcDataFlags(BaseUnion):
    _fields_ = [
        ('all', c_ulong),
        ('bits', AcdpPcDataFlagsBits)
    ]


class AcdpPcDataCtrlFlagsBits(BaseStructure):
    _fields_ = [
        ('ctrl_ok', c_bool),      # 0
        ('running', c_bool),      # 1
        ('em_stop', c_bool),      # 2
        ('fast_stop', c_bool),    # 3
    ]


class AcdpPcDataCtrlFlags(BaseUnion):
    _fields_ = [
        ('all', c_ulong),
        ('bits', AcdpPcDataCtrlFlagsBits)
    ]


class AcdpPcDataCtrlLocIODI16Pins(BaseStructure):
    _fields_ = [
        ('run_test', c_bool),
        ('move_up_crossbar', c_bool),
        ('move_down_crossbar', c_bool),
        ('move_to_start', c_bool)
    ]


class AcdpPcDataCtrlLocIODI16(BaseUnion):
    _fields_ = [
        ('all', c_uint16),
        ('pins', AcdpPcDataCtrlLocIODI16Pins)
    ]


class AcdpPcDataCtrlLocIODO16Pins(BaseStructure):
    _fields_ = [
        ('test_cancelled_ind', c_bool),
        ('test_out_of_tolerance_ind', c_bool),
        ('test_ok_ind', c_bool),
        ('test_running_ind', c_bool)
    ]


class AcdpPcDataCtrlLocIODO16(BaseUnion):
    _fields_ = [
        ('all', c_uint16),
        ('pins', AcdpPcDataCtrlLocIODO16Pins)
    ]


class AcdpPcDataCtrlLocIO(BaseStructure):
    _fields_ = [
        ('di16', AcdpPcDataCtrlLocIODI16),
        ('do16', AcdpPcDataCtrlLocIODO16)
    ]


class AcdpPcDataCtrlRemIODI16Enums:     # Remote Digital Inputs
    ID_X_DI_0    = 0
    ID_X_DI_1    = 1
    CANT_DIS   = 2


class AcdpPcDataCtrlRemIODI16Inputs(BaseStructure):
    _fields_ = [
        ('i0', c_bool)  # 0
    ]


class AcdpPcDataCtrlRemIODI16(BaseUnion):
    _fields_ = [
        ('all', c_uint16),
        ('di', AcdpPcDataCtrlRemIODI16Inputs)
    ]


class AcdpPcDataCtrlRemIODO16Enums:     # Remote Digital Outputs
    ID_X_DO_0   = 0
    ID_X_DO_1   = 1
    CANT_DOS    = 2


class AcdpPcDataCtrlRemIODO16DO(BaseStructure):
    _fields_ = [
        ('o0', c_bool)  # 0
    ]


class AcdpPcDataCtrlRemIODO16(BaseUnion):
    _fields_ = [
        ('all', c_uint16),
        ('do', AcdpPcDataCtrlRemIODO16DO)
    ]


class AcdpPcDataCtrlRemIODI16Array(ctypes.Array):
    _length_ = AcdpPcDataCtrlRemIODI16Enums.CANT_DIS
    _type_ = AcdpPcDataCtrlRemIODI16


class AcdpPcDataCtrlRemIODO16Array(ctypes.Array):
    _length_ = AcdpPcDataCtrlRemIODO16Enums.CANT_DOS
    _type_ = AcdpPcDataCtrlRemIODO16


class AcdpPcDataCtrlRemIO(BaseStructure):
    _fields_ = [
        ('di16', AcdpPcDataCtrlRemIODI16Array),
        ('do16', AcdpPcDataCtrlRemIODO16Array)
    ]


class AcdpAxisMovementsMovEjeDataArray(ctypes.Array):
    _length_ = AcdpAxisMovementEnums.CANT_EJES
    _type_ = AcdpAxisMovementsMovEjeData


class AcdpPcDataCtrl(BaseStructure):
    _fields_ = [
        ('flags', AcdpPcDataCtrlFlags),
        ('loc_io', AcdpPcDataCtrlLocIO),    # Local Inputs/Outpus
        ('rem_io', AcdpPcDataCtrlRemIO),    # Remote Inputs/Outputs

        ('eje', AcdpAxisMovementsMovEjeDataArray)
    ]


class AcdpPcData(BaseStructure):
    _fields_ = [
        ('flags', AcdpPcDataFlags),
        ('ctrl', AcdpPcDataCtrl)
    ]


class AcdpPc(BaseStructure):
    _fields_ = [
        ('data', AcdpPcData)
    ]

    def store_from_raw(self, raw_values):
        super().store_from_raw(raw_values)
        
        # Command flags
        self.cmd_toggle = self.data.flags.bits.cmd_toggle
        self.cmd_received = self.data.flags.bits.cmd_received

        # Control flags
        self.ctrl_ok = self.data.ctrl.flags.bits.ctrl_ok
        self.running = self.data.ctrl.flags.bits.running
        self.em_stop = self.data.ctrl.flags.bits.em_stop
        self.fast_stop = self.data.ctrl.flags.bits.fast_stop

        # Local digital inpunts/outputs
        self.run_test = self.data.ctrl.loc_io.di16.pins.run_test,
        self.move_up_crossbar = self.data.ctrl.loc_io.di16.pins.move_up_crossbar,
        self.move_down_crossbar = self.data.ctrl.loc_io.di16.pins.move_down_crossbar,
        self.move_to_start = self.data.ctrl.loc_io.di16.pins.move_to_start
        
        self.test_cancelled_ind = self.data.ctrl.loc_io.do16.pins.test_cancelled_ind,
        self.test_out_of_tolerance_ind = self.data.ctrl.loc_io.do16.pins.test_out_of_tolerance_ind,
        self.test_ok_ind = self.data.ctrl.loc_io.do16.pins.test_ok_ind,
        self.test_running_ind = self.data.ctrl.loc_io.do16.pinstest_running_ind

        # Remote digital inputs/outputs
        self.rem_di = []
        for i in range(self.data.ctrl.rem_io.di16._length_):
            self.rem_di.append(self.ctrl.rem_io.di16[i].all)
        
        self.rem_do = []
        for i in range(self.data.ctrl.rem_io.do16._length_):
            self.rem_do.append(self.ctrl.rem_io.do16[i].all)

        # Axis
        self.axis = []
        for i in range(self.data.ctrl.eje._length_):
            axis = self.get_axis(i)
            self.axis.append({
                # Flags
                'flags': axis.flags.all,
                'em_stop_flag': axis.flags.flags.em_stop,
                'disabled_flag': axis.flags.flags.disabled,
                'sync_on_flag': axis.flags.flags.sync_on,
                
                # States machine
                'flags_fin': axis.maq_est.flags_fin,
                'state': axis.maq_est.estado,

                # Position movement
                'mov_pos_homing_states': axis.mov_pos.homing.estado,
                'pos_flags': axis.mov_pos.flags,
                'pos_pos_fil': axis.mov_pos.med_drv.pos_fil,
                'pos_vel_fil': axis.mov_pos.med_drv.vel_fil,

                # Load
                'load_flags': axis.mov_pos.mead_load.enc.flags.all,
                'load_pos_fil': axis.mov_pos.med_load.pos_vil,
                'load_vel_fil': axis.mov_pos.med_load.vel_fil,

                # Sincro
                'rel_master': axis.sincro.rel_master,
                'set_point_dif': axis.sincro.set_point_dif,
                'med_drv_modulo': axis.sincro.med_drv.modulo,
                'pos_dif': axis.sincro.med_drv.pos_dif,
                'vel_dif': axis.sincro.med_drv.vel_dif,

                # Force
                'fza_flags': axis.mov_fza.flags.all,
                'fza_fil': axis.mov_fza.fza_fil,
                'rigidez_drive': axis.mov_fza.rigidez_drive,
                'rigidez_load': axis.mov_fza.rigidez_load,
                'cedencia': axis.mov_fza.cedencia,
                'rel_fza_pos_uns': axis.mov_fza.rel_fza_pos_uns,

                # Drive
                'drv_flags': axis.drive.flags.all,
                'actuacion': axis.drive.actiacion
            })


    def get_load_axis(self):
        return self.data.ctrl.eje[AcdpAxisMovementEnums.ID_X_EJE_CARGA]
    
    def get_turn_axis(self):
        return self.data.ctrl.eje[AcdpAxisMovementEnums.ID_X_EJE_GIRO]
    
    def get_thrust_axis(self):
        return self.data.ctrl.eje[AcdpAxisMovementEnums.ID_X_EJE_AVANCE]
    
    def get_axis(self, axis):
        if axis == AcdpAxisMovementEnums.ID_X_EJE_CARGA:
            return self.get_load_axis()

        elif axis == AcdpAxisMovementEnums.ID_X_EJE_GIRO:
            return self.get_turn_axis()
        
        elif axis == AcdpAxisMovementEnums.ID_X_EJE_AVANCE:
            return self.get_thrust_axis()
        
        else:
            print("Eje no encontrado")
            return False
    
    def get_axis_states(self, axis):
        states = self.get_axis(axis).maq_est
        return states
    
    def get_axis_flags(self, axis):
        flags = self.get_axis(axis).flags
        return flags