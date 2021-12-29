# coding=utf-8
import struct, ctypes
from ctypes import Structure, Union, c_uint32, c_float, c_bool, c_long, c_ulong


class BaseStructure(Structure):

    empty = True
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.data_length = self.get_len()
        self.bytes_length = self.get_bytes_size()

    def get_format(self):
        str_format = ''
        f = ''
        for field in self._fields_:
            field_value = field[1]

            if issubclass(field_value, ctypes._SimpleCData):
                f = field_value._type_

            elif issubclass(field_value, ctypes.Array):
                element = getattr(self, field[0])
                f = element[0].get_format() * field[1]._length_
            
            elif field_value:
                f = field_value().get_format()

            str_format = ''.join((str_format, f))
        return str_format

    def get_bytes_size(self):
        # return ctypes.sizeof(self)
        return struct.calcsize(self.get_format())

    def get_values(self):   # Returns a tuple with structure values
        values = ()
        for field in self._fields_:
            field_value = field[1]
            field_name = field[0]
            value = ()

            if issubclass(field_value, ctypes._SimpleCData):
                value = (getattr(self, field_name),)
            
            elif issubclass(field_value, ctypes.Array):
                arr = getattr(self, field_name)
                for j in range(field_value._length_):
                    value = sum((value, arr[j].get_values()), ())
            
            else:       # BaseStructure
                value = getattr(self, field_name).get_values()
            
            values = sum((values, value), ())

        return values

    def get_len(self):
        return len(self.get_values())

    def store_values(self, values):     # Receives values in tuple to store

        i = 0

        for field in self._fields_:
            field_type = field[1]
            field_name = field[0]

            if issubclass(field_type, ctypes._SimpleCData):
                value = values[i]
                setattr(self, field_name, value)
                i = i + 1

            elif field_type:
                if issubclass(field_type, ctypes.Array):
                    aux = getattr(self, field[0])
                    for aux_field in aux:
                        value = aux_field()
                        field_len = value.get_len()
                        value.store_values(values[i:(i+field_len)])
                        setattr(self, field_name, value)
                        i = i + field_len
                else:
                    vals = field_type()
                    field_len = vals.get_len()
                    vals.store_values(values[i:(i+field_len)])
                    setattr(self, field_name, vals)
                    i = i + field_len

    def pacself(self):    # Returns structure in bytes format
        frm = self.get_format()
        values = self.get_values()
        data = b''
        for i in range(0, len(frm)):
            f = frm[i]
            value = values[i]
            data = b''.join([data, struct.pack(f, value)])
        return data

    def unpacdata(self, raw_data):
        unpacked_data = struct.unpack(self.get_format(), raw_data)
        return unpacked_data

    def store_from_raw(self, raw_values):
        self.store_values(self.unpacdata(raw_data=raw_values))

    def to_dict(self):

        dict = {}
        for field in self._fields_:
            field_type = field[1]
            key = field[0]
            value = getattr(self, key)

            if not issubclass(field_type, ctypes._SimpleCData):
                aux_dict = value.to_dict()
                value = aux_dict

            dict[key] = value

        return dict


class BaseUnion(Union):     # Mostly used for flags
    def get_format(self, field_name=''):    # Get string format for pack/unpack
        fields = self._fields_

        if field_name:      # Only used on AcdpDrvCmdConfigUnion
            index = self.get_field_index(field_name)
            return self._fields_[index][1].get_format()
        
        else:
            field_type = fields[0][1]   # First always indicates the union size
            if issubclass(field_type, ctypes._SimpleCData):
                return field_type._type_
            else:
                field_type.get_format()


    def get_bytes_size(self):
        return struct.calcsize(self.get_format())

    def get_len(self):
        return len(self.get_values())

    def get_values(self, field_name=''):   # Returns a tuple with values
        if field_name:
            value = getattr(self, field_name)
            return value.get_values()
        else:
            field = self._fields_[0]
            if issubclass(field[1], ctypes._SimpleCData):
                return (getattr(self, field[0]),)
            else:
                field[1].get_values()
    
    def store_values(self, values, field_name=''):     # Receives values in tuple to store

        if field_name:
            getattr(self, field_name).store_values(values)

        else:
            field = self._fields_[0]
            if issubclass(field[1], ctypes._SimpleCData):
                setattr(self, field[0], values[0])
            else:
                field[1].store_values(values)

    def pacself(self):    # Returns structure in bytes format
        frm = self.get_format()
        values = self.get_values()
        data = b''
        for i in range(0, len(frm)):
            f = frm[i]
            value = values[i]
            data = b''.join([data, struct.pack(f, value)])
        return data

    def unpacdata(self, raw_data):
        unpacked_data = struct.unpack(self.get_format(), raw_data)
        return unpacked_data

    def store_from_raw(self, raw_values):
        self.store_values(self.unpacdata(raw_data=raw_values))

    def to_dict(self):
        dict = {}
        for field in self._fields_:
            field_type = field[1]
            key = field[0]
            value = getattr(self, key)

            if not issubclass(field_type, ctypes._SimpleCData):
                aux_dict = value.to_dict()
                value = aux_dict

            dict[key] = value

        return dict
    
    def get_field_index(self, field_name):
        index = [i for i, tupl in enumerate(self._fields_) if tupl[0] == field_name]
        if len(index) > 0:
            return index[0]
        else:
            raise Exception('Field name not found.')


# --------------------------------------------------------------------------------------------#
# -------------------------------- Códigos de Mensajes ---------------------------------------#
# --------------------------------------------------------------------------------------------#


class AcdpMsgType:
    SYS       = 0x0000   # Sistema
    CXN       = 0x1000   # Conexion
    CMD       = 0x2000   # Comandos
    DATA      = 0x3000   # Datos
    CFG_SET   = 0x4000   # Seteo configuracion
    CFG_REQ   = 0x5000   # Solicitud configuracion
    CFG_DAT   = 0x6000   # Datos de configuracion


class AcdpMsgLevel:
    BASE          = 0x0000
    DEVICE        = 0x0100
    APPLICATION   = 0x0200


class AcdpMsgCxn:       # Connection
    CD_CONNECT             = AcdpMsgType.CXN + AcdpMsgLevel.BASE + 0x01
    CD_DISCONNECT          = AcdpMsgType.CXN + AcdpMsgLevel.BASE + 0x02
    CD_CONNECTION_STAT     = AcdpMsgType.CXN + AcdpMsgLevel.BASE + 0x03
    CD_FORCE_CONNECT       = AcdpMsgType.CXN + AcdpMsgLevel.BASE + 0x04
    CD_ECHO_REQ            = AcdpMsgType.CXN + AcdpMsgLevel.BASE + 0x05
    CD_ECHO_REPLY          = AcdpMsgType.CXN + AcdpMsgLevel.BASE + 0x06
    CD_ECHO_TIMEOUT        = AcdpMsgType.CXN + AcdpMsgLevel.BASE + 0x07
    CD_RTCSYNC_REQ         = AcdpMsgType.CXN + AcdpMsgLevel.BASE + 0x08
    CD_RTCSYNC_REPLY       = AcdpMsgType.CXN + AcdpMsgLevel.BASE + 0x09
    CD_CONFIG_REQ          = AcdpMsgType.CXN + AcdpMsgLevel.BASE + 0x0A
    CD_CONFIG_DAT          = AcdpMsgType.CXN + AcdpMsgLevel.BASE + 0x0B
    CD_CONFIG_SETDEFAULT   = AcdpMsgType.CXN + AcdpMsgLevel.BASE + 0x0C
    CD_IPCONFIG_SET        = AcdpMsgType.CXN + AcdpMsgLevel.BASE + 0x0D
    CD_CTRL_CONFIG_SET     = AcdpMsgType.CXN + AcdpMsgLevel.BASE + 0x0E
    CD_CTRL_CONFIG_CLR     = AcdpMsgType.CXN + AcdpMsgLevel.BASE + 0x0F
    CD_RTC_OFFSET_SET      = AcdpMsgType.CXN + AcdpMsgLevel.BASE + 0x10
    CD_ECAT_VLAN_ID_SET    = AcdpMsgType.CXN + AcdpMsgLevel.BASE + 0x11


class AcdpMsgCfgSet:
    CD_SUCCESSFUL          = AcdpMsgType.CFG_SET + AcdpMsgLevel.BASE + 0x01
    CD_REJECTED            = AcdpMsgType.CFG_SET + AcdpMsgLevel.BASE + 0x02
    CD_DEFAULT             = AcdpMsgType.CFG_SET + AcdpMsgLevel.BASE + 0x03
    CD_RESTORE_FROM_FLASH  = AcdpMsgType.CFG_SET + AcdpMsgLevel.BASE + 0x04
    CD_SAVE_TO_FLASH       = AcdpMsgType.CFG_SET + AcdpMsgLevel.BASE + 0x05
    CD_AVI                 = AcdpMsgType.CFG_SET + AcdpMsgLevel.BASE + 0x06      # Parametro: Acdp::Avi::tConfig
    CD_ENC                 = AcdpMsgType.CFG_SET + AcdpMsgLevel.BASE + 0x07      # Parametro: Acdp::Enc::tConfig
    CD_DRV_FBK             = AcdpMsgType.CFG_SET + AcdpMsgLevel.BASE + 0x08      # Parametro: Acdp::DrvFbk::tConfig
    CD_DRV_ECAT            = AcdpMsgType.CFG_SET + AcdpMsgLevel.BASE + 0x09      # Parametro: Acdp::DrvCmd::tConfig
    CD_DRV_ANA             = AcdpMsgType.CFG_SET + AcdpMsgLevel.BASE + 0x0a      # Parametro: Acdp::DrvCmd::tConfig
    CD_DRV_PULSE           = AcdpMsgType.CFG_SET + AcdpMsgLevel.BASE + 0x0b      # Parametro: Acdp::DrvCmd::tConfig


class AcdpMsgCfgReq:
    kCd_Rejected    = AcdpMsgType.CFG_REQ + AcdpMsgLevel.BASE + 0x01
    kCd_Avi         = AcdpMsgType.CFG_REQ + AcdpMsgLevel.BASE + 0x02
    kCd_Enc         = AcdpMsgType.CFG_REQ + AcdpMsgLevel.BASE + 0x03
    kCd_DrvFbk      = AcdpMsgType.CFG_REQ + AcdpMsgLevel.BASE + 0x04
    kCd_DrvEcat     = AcdpMsgType.CFG_REQ + AcdpMsgLevel.BASE + 0x05
    kCd_DrvAna      = AcdpMsgType.CFG_REQ + AcdpMsgLevel.BASE + 0x06
    kCd_DrvPulse    = AcdpMsgType.CFG_REQ + AcdpMsgLevel.BASE + 0x07


class AcdpMsgCfgDat:
    CD_AVI         = AcdpMsgType.CFG_DAT + AcdpMsgLevel.BASE + 0x01     # Dato: Acdp::Avi::tConfig
    CD_ENC         = AcdpMsgType.CFG_DAT + AcdpMsgLevel.BASE + 0x02     # Dato: Acdp::Enc::tConfig
    CD_DRVFBK      = AcdpMsgType.CFG_DAT + AcdpMsgLevel.BASE + 0x03     # Dato: Acdp::DrvFbk::tConfig
    CD_DRVECAT     = AcdpMsgType.CFG_DAT + AcdpMsgLevel.BASE + 0x04     # Dato: Acdp::DrvCmd::tConfig
    CD_DRVANA      = AcdpMsgType.CFG_DAT + AcdpMsgLevel.BASE + 0x05     # Dato: Acdp::DrvCmd::tConfig
    CD_DRVPULSE    = AcdpMsgType.CFG_DAT + AcdpMsgLevel.BASE + 0x06     # Dato: Acdp::DrvCmd::tConfig


class AcdpMsgData:
    CD_ALL     = AcdpMsgType.DATA + AcdpMsgLevel.BASE + 0x01    # Dato: Acdp::tData
    CD_AVI     = AcdpMsgType.DATA + AcdpMsgLevel.BASE + 0x02    # Dato: Acdp::Avi::tData
    CD_ENC     = AcdpMsgType.DATA + AcdpMsgLevel.BASE + 0x03    # Dato: Acdp::Enc::tData
    CD_DRVFBK  = AcdpMsgType.DATA + AcdpMsgLevel.BASE + 0x04    # Dato: Acdp::DrvFbk::tData
    CD_DRVCMD  = AcdpMsgType.DATA + AcdpMsgLevel.BASE + 0x05    # Dato: Acdp::DrvCmd::tData


class AcdpMsgCmdParamSetTareAvi(BaseStructure):
    _fields_ = [
        ('Tare', c_float)
    ]


class AcdpMsgCmdParamSetZeroEnc(BaseStructure):
    _fields_ = [
        ('Zero', c_float)
    ]


class AcdpMsgCmdParamSetZeroDrvFbk(BaseStructure):
    _fields_ = [
        ('Zero', c_float)
    ]


class AcdpMsgCmdParam(BaseStructure):
    _fields_ = [
        ('set_tare_avi', AcdpMsgCmdParamSetTareAvi),
        ('set_zero_enc', AcdpMsgCmdParamSetZeroEnc),
        ('set_zero_drvFbk', AcdpMsgCmdParamSetZeroDrvFbk)
    ]


class AcdpMsgCmd:
    CD_REJECTED           = AcdpMsgType.CMD + AcdpMsgLevel.BASE + 0x01
    CD_ENTER_SAFE_MODE    = AcdpMsgType.CMD + AcdpMsgLevel.BASE + 0x02
    CD_EXIT_SAFE_MODE     = AcdpMsgType.CMD + AcdpMsgLevel.BASE + 0x03
    CD_STOP_ALL           = AcdpMsgType.CMD + AcdpMsgLevel.BASE + 0x04
    CD_SET_TARE_AVI       = AcdpMsgType.CMD + AcdpMsgLevel.BASE + 0x05  # Parametro: Param::tSetTareAvi
    CD_SET_ZERO_ENC       = AcdpMsgType.CMD + AcdpMsgLevel.BASE + 0x06  # Parametro: Param::tSetZeroEnc
    CD_SET_ZERO_DRVF_BK   = AcdpMsgType.CMD + AcdpMsgLevel.BASE + 0x07  # Parametro: Param::tSetZeroDrvFbk
    Param                 = AcdpMsgCmdParam


class AcdpMsg:
    kTypeMsk    = 0xf000
    kLevelMsk   = 0x0f00
    Type        = AcdpMsgType
    Level       = AcdpMsgLevel
    Cxn         = AcdpMsgCxn
    CfgSet      = AcdpMsgCfgSet
    CfgReq      = AcdpMsgCfgReq
    CfgDat      = AcdpMsgCfgDat
    Data        = AcdpMsgData
    Cmd         = AcdpMsgCmd


# --------------------------------------------------------------------------------------------#
# -------------------------------- Entrada Analogica -----------------------------------------#
# --------------------------------------------------------------------------------------------#


class AcdpAviConfigFlagsBits(BaseStructure):
    _fields_ = [
        ('inv_sign', c_bool)
    ]

class AcdpAviConfigFlags(BaseUnion):
    _fields_ = [
        ('all', c_ulong),
        ('flags', AcdpAviConfigFlagsBits)
    ]


class AcdpAviConfigCalib(BaseStructure):
    _fields_ = [
        ('m', c_float),
        ('zero', c_float)
    ]


class AcdpAviConfig(BaseStructure):
    _fields_ = [
        ('flags', AcdpAviConfigFlags),
        ('calib', AcdpAviConfigCalib)
    ]


class AcdpAviData(BaseStructure):
    _fields_ = [
        ('tare', c_float),
        ('value', c_float)
    ]


class AcdpAvi(BaseStructure):
    _fields_ = [
        ('t_config', AcdpAviConfig),
        ('t_data', AcdpAviData)
    ]


# --------------------------------------------------------------------------------------------#
# -------------------------------------- Encoder ---------------------------------------------#
# --------------------------------------------------------------------------------------------#


class AcdpEncConfigFlagsBits(BaseStructure):
    _fields_ = [
        ('inv_med', c_ulong),
        ('modulo', c_ulong),
        ('absolute', c_ulong),
        ('non_volatile_zero', c_ulong),
        ('absolute_zero_settled', c_ulong)
    ]


class AcdpEncConfigFlags(BaseUnion):
    _fields_ = [
        ('all', c_ulong),
        ('bits', AcdpEncConfigFlagsBits)
    ]


class AcdpEncConfig(BaseStructure):
    _fields_ = [
        ('flags', AcdpEncConfigFlags),
        ('resolution', c_ulong),
        ('range', c_float),
        ('zero', c_float),
        ('offset', c_float)
    ]


class AcdpEncDataFlagsBits(BaseStructure):
    _fields_ = [
        ('ready', c_bool),
        ('enabled', c_bool),
        ('fault', c_bool),
        ('positive_0t', c_bool),
        ('negative_0t', c_bool),
        ('home_switch', c_bool),
        ('homing_ended_ok', c_bool),
        ('homing_error', c_bool),
        ('zero_settled', c_bool),
        ('unknown_zero', c_bool),
        ('pos_dec', c_bool),
        ('time_0v_pulso', c_bool),
    ]

class AcdpEncDataFlags(BaseUnion):
    _fields_ = [
        ('all', c_ulong),
        ('bits', AcdpEncDataFlagsBits)
    ]

class AcdpEncData(BaseStructure):
    _fields_ = [
        ('flags', AcdpEncDataFlags),

        ('int_stamp', c_ulong),
        ('int_pos_abs', c_long),
        ('int_pos_abs_cross', c_long),

        ('config', AcdpEncConfig),
        ('pos_abs', c_float),
        ('pos', c_float),
        ('vel', c_float)
    ]


class AcdpEnc:
    _fields_ = [
        ('config', AcdpEncConfig),
        ('data', AcdpEncData)
    ]


# --------------------------------------------------------------------------------------------#
# ----------------------------------- Drive Feedback -----------------------------------------#
# --------------------------------------------------------------------------------------------#


class AcdpDrvFbkConfigFlagsBits(BaseStructure):
    _fields_ = [
        ('inv_med', c_bool),
        ('modulo', c_bool),
        ('absolute', c_bool),
        ('non_volatile_zero', c_bool),
        ('absolute_zero_settled', c_bool),
    ]


class AcdpDrvFbkConfigFlags(BaseUnion):
    _fields_ = [
        ('all', c_ulong),
        ('bits', AcdpDrvFbkConfigFlagsBits)
    ]


class AcdpDrvFbkConfigPos(BaseStructure):
    _fields_ = [
        ('rsl', c_long),        # Resolution
        ('range', c_float),
        ('zero', c_float),
        ('offset', c_float)
    ]


class AcdpDrvFbkConfigVel(BaseStructure):
    _fields_ = [
        ('rsl', c_ulong),      # Resolution
        ('range', c_float)
    ]


class AcdpDrvFbkConfig(BaseStructure):
    _fields_ = [
        ('flags', AcdpDrvFbkConfigFlags),
        ('pos', AcdpDrvFbkConfigPos),
        ('vel', AcdpDrvFbkConfigVel)
    ]


class AcdpDrvFbkDataFlagsBits(BaseStructure):
    _fields_ = [
        ('ready', c_bool),
        ('enabled', c_bool),
        ('fault', c_bool),
        ('positive_0t', c_bool),
        ('negative_0t', c_bool),
        ('home_switch', c_bool),
        ('homming_ended_ok', c_bool),
        ('homming_error', c_bool),
        ('zero_settled', c_bool),
        ('unknown_zero', c_bool)
    ]


class AcdpDrvFbkDataFlags(BaseUnion):
    _fields_ = [
        ('all', c_ulong),
        ('bits', AcdpDrvFbkDataFlagsBits)
    ]


class AcdpDrvFbkData(BaseStructure):
    _fields_ = [
        ('flags', AcdpDrvFbkDataFlags),

        ('config', AcdpDrvFbkConfig),
        ('pos_abs', c_float),           # Pos sin cerar
        ('pos', c_float),
        ('vel', c_float)                # [mm/s]
    ]


class AcdpDrvFbk(BaseStructure):
    _fields_ = [
        ('config', AcdpDrvFbkConfig),
        ('data', AcdpDrvFbkData)
    ]


# --------------------------------------------------------------------------------------------#
# ------------------------------------ Drive Comando -----------------------------------------#
# --------------------------------------------------------------------------------------------#


class AcdpDrvCmdConfigFlagsBits(BaseStructure):
    _fields_ = [
        ('ana_ref_bipolar', c_bool),
        ('invertir_sentido', c_bool),
        ('chk_fbk_enab', c_bool),
        ('homing_enabled', c_bool),
    ]


class AcdpDrvCmdConfigFlags(BaseUnion):
    _fields_ = [
        ('all', c_ulong),
        ('bits', AcdpDrvCmdConfigFlagsBits)
    ]


class AcdpDrvCmdConfigUnionAna(BaseStructure):
    _fields_ = [
        ('vel_fsd', c_float)    # [mm/s] - [Hz] - Para ref analogica
    ]


class AcdpDrvCmdConfigUnionPulse(BaseStructure):
    _fields_ = [
        ('paso_pos', c_float),          # [mm] - Para ref de pulsos
        ('prd_pulso_max', c_float)      # [s] - Para ref de pulsos (para evitar que el tiempo de pulso genere inestabilidad en el control)
    ]


class AcdpDrvCmdConfigUnionEcatVel(BaseStructure):
    _fields_ = [
        ('rsl', c_ulong),
        ('range', c_float)
    ]


class AcdpDrvCmdUnionEcat(BaseStructure):
    _fields_ = [
        ('ecat', AcdpDrvCmdConfigUnionEcatVel)
    ]


class AcdpDrvCmdConfigUnion(BaseUnion):
    _fields_ = [
        ('ana', AcdpDrvCmdConfigUnionAna),
        ('pulse', AcdpDrvCmdConfigUnionPulse),
        ('vel', AcdpDrvCmdUnionEcat)
    ]


class AcdpDrvCmdConfigChkFbk(BaseStructure):
    _fields_ = [
        ('error_max', c_float),
        ('delta_t', c_float)
    ]


class AcdpDrvCmdConfig(BaseStructure):      # Configuracion Drive
    _fields_ = [
        ('flags', AcdpDrvCmdConfigFlags),
        ('union', AcdpDrvCmdConfigUnion),
        ('chk_fbk', AcdpDrvCmdConfigChkFbk),
        ('tau_filtro', c_float)
    ]


class AcdpDrvCmdDataFlagsBits(BaseStructure):
    _fields_ = [
        ('pow_enabled', c_bool),
        ('homing', c_bool),
        ('pos_feedback_error', c_bool),
        ('limit_vel_max', c_bool),
        ('limit_vel_min', c_bool)
    ]


class AcdpDrvCmdDataFlags(BaseUnion):
    _fields_ = [
        ('all', c_ulong),
        ('bits', AcdpDrvCmdDataFlagsBits)
    ]


class AcdpDrvCmdData(BaseStructure):        # Datos Drive
    _fields_ = [
        ('flags', AcdpDrvCmdDataFlags),
        ('actuacion', c_float)
    ]


class AcdpDrvCmd(BaseStructure):
    _fields_ = [
        ('config', AcdpDrvCmdConfig),
        ('data', AcdpDrvCmdData)
    ]


# --------------------------------------------------------------------------------------------#
# --------------- Control automatico PI Tipo 0 ([Actuacion/Referencia] = 1) ------------------#
# --------------------------------------------------------------------------------------------#


class AcdpPiT0ConfigFf(BaseStructure):  # Factor Feedforward (Rango de 0 a 1)
    _fields_ = [
        ('k', c_float)
    ]


class AcdpPiT0ConfigPid(BaseStructure):
    _fields_ = [
        ('tau', c_float),   # [s]
        ('k', c_float)      # [-]
    ]


class AcdpPiT0ConfigOut(BaseStructure):
    _fields_ = [
        ('max', c_float)
    ]


class AcdpPiT0Config(BaseStructure):    # Configuracion control automatico PI Tipo 0
    _fields_ = [
        ('ff', AcdpPiT0ConfigFf),
        ('pid', AcdpPiT0ConfigPid),
        ('tiempo_fin', c_float),
        ('out', AcdpPiT0ConfigOut)
    ]


class AcdpPiT0DataFf(BaseStructure):
    _fields_ = [
        ('out', c_float)
    ]


class AcdpPiT0DataPid(BaseStructure):
    _fields_ = [
        ('integ_out', c_float),
        ('prop_out', c_float)
    ]


class AcdpPiT0Data(BaseStructure):    # Datos control automatico PI Tipo 0
    _fields_ = [
        ('ref', c_float),
        ('ff', AcdpPiT0DataFf),
        ('pid', AcdpPiT0DataPid),
        ('out', c_float)
    ]


class AcdpPiT0(BaseStructure):
    _fields_ = [
        ('config', AcdpPiT0Config),
        ('data', AcdpPiT0Data)
    ]


# --------------------------------------------------------------------------------------------#
# ------------ Control automatico PID Tipo 1 ([Actuacion/Referencia] = 1/s) ------------------#
# --------------------------------------------------------------------------------------------#


class AcdpPiT1ConfigRef(BaseStructure):     # Cero desactiva el limite (Limite para la derivada de la referencia)
    _fields_ = [
        ('slope_max_deriv', c_float)
    ]


class AcdpPiT1ConfigFf(BaseStructure):
    _fields_ = [
        ('k', c_float)                      # Factor Feedforward (Rango de 0 a 1)
    ]


class AcdpPiT1ConfigPid(BaseStructure):
    _fields_ = [
        ('tau_i', c_float),                 # [s]
        ('tau_p', c_float),                 # [s]
        ('k', c_float)                      # [-]
    ]


class AcdpPidT1Config(BaseStructure):        # Configuracion control automatico PID Tipo 1
    _fields_= [
        ('ref', AcdpPiT1ConfigRef),
        ('ff', AcdpPiT1ConfigFf),
        ('pid', AcdpPiT1ConfigPid),
        ('tiempo_fin', c_float),
        ('error_final', c_float)
    ]


class AcdpPiT1DataFf(BaseStructure):
    _fields_ = [
        ('out', c_float)
    ]


class AcdpPiT1DataPid(BaseStructure):
    _fields_ = [
        ('integ_out', c_float),
        ('prop_out', c_float),
        ('deriv_out', c_float)
    ]


class AcdpPidT1Data(BaseStructure):          # Datos control automatico PID Tipo 1
    _fields_= [
        ('ref', c_float),
        ('ff', AcdpPiT1DataFf),             # Derivada de la referencia
        ('pid', AcdpPiT1DataPid),
        ('out', c_float)
    ]


class AcdpPidT1(BaseStructure):
    _fields_ = [
        ('config', AcdpPidT1Config),
        ('data', AcdpPidT1Data)
    ]


# ------------------------------------------------------------------------------------#

class Acpd:
    Msg     = AcdpMsg
    Avi     = AcdpAvi
    Enc     = AcdpEnc
    DrvFbk  = AcdpDrvFbk
    DrvCmd  = AcdpDrvCmd