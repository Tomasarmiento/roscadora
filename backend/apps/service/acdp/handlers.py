from .acdp import ACDP_VERSION, ACDP_UDP_PORT, ACDP_IP_ADDR
from .acdp import AcdpHeader
from .messages_app import AcdpPc, AcdpMsgCodes, AcdpMsgParams, AcdpAxisMovementEnums
from .messages_base import AcdpMsgCmdParam, BaseStructure, AcdpMsgCxn

class AcdpMessage(BaseStructure):
    last_rx_data = AcdpPc()
    last_rx_header = AcdpHeader()

    _fields_ = [
        ('header', AcdpHeader),
        ('data', AcdpPc)
    ]

    def get_msg_id(self):
        return self.header.ctrl.msg_id

    def store_from_raw(self, raw_values):
        bytes_len = len(raw_values)
        if bytes_len == self.header.get_bytes_size():
            self.header.store_from_raw(raw_values)
        else:
            super().store_from_raw(raw_values)
    
    def process_rx_msg(self, addr=(ACDP_IP_ADDR, ACDP_UDP_PORT), transport=None):
        msg_code = self.header.get_msg_code()
        
        if msg_code == AcdpMsgCxn.CD_ECHO_REQ:
            tx_header = build_header(AcdpMsgCxn.CD_ECHO_REPLY)
            transport.sendto(tx_header.pacself(), addr)


def build_header(code, host_ip="192.168.0.100", dest_ip=ACDP_IP_ADDR, *args, **kwargs):

    tx_header = AcdpHeader()
    tx_header.ctrl.msg_code = code

    tx_header.ctrl.msg_code = code
    tx_header.version = ACDP_VERSION
    tx_header.channel = 0
    tx_header.ip_addr.store_from_string(host_ip)
    tx_header.dest_addr.store_from_string(dest_ip)

    tx_header.ctrl.device_type = 0
    tx_header.ctrl.firmware_version = 0
    tx_header.ctrl.object = 0
    tx_header.ctrl.flags = 0
    tx_header.ctrl.timestamp = 0

    if code == AcdpMsgCxn.CD_FORCE_CONNECT or code == AcdpMsgCxn.CD_DISCONNECT \
        or code == AcdpMsgCxn.CD_CONNECT or code == AcdpMsgCxn.CD_ECHO_REPLY:     # open/close/force connection / echo reply
        tx_header.ctrl.msg_id = 0
        tx_header.ctrl.data_len8 = 0
    
    elif code == AcdpMsgCodes.Cmd.Cd_MovEje_RunZeroing:
        axis = kwargs['eje']
        tx_header.ctrl.object = axis

    elif code == AcdpMsgCodes.Cmd.Cd_MovEje_Stop:
        tx_header.set_msg_id(msg_id=kwargs['msg_id'])
    
    else:
        tx_header.set_msg_id(msg_id=kwargs['msg_id'])
        tx_header.ctrl.object = AcdpAxisMovementEnums.ID_X_EJE_AVANCE
        params = AcdpMsgParams()

        if code == AcdpMsgCodes.Cmd.Cd_MovEje_SyncOn:
            param = params.sync_on
        
        elif code == AcdpMsgCodes.Cmd.Cd_MovEje_MovToVel:
            param = params.mov_to_vel

        elif code == AcdpMsgCodes.Cmd.Cd_MovEje_MovToPos:
            param =  params.mov_to_pos

        elif code == AcdpMsgCodes.Cmd.Cd_MovEje_MovToPos_Yield:
            param =  params.mov_to_pos_yield

        elif code == AcdpMsgCodes.Cmd.Cd_MovEje_MovToPosLoad:
            param =  params.mov_to_pos_load

        elif code == AcdpMsgCodes.Cmd.Cd_MovEje_MovToPosLoad_Yield:
            param =  params.mov_to_pos_load_yield

        elif code == AcdpMsgCodes.Cmd.Cd_MovEje_MovToFza:
            param =  params.mov_to_fza

        elif code == AcdpMsgCodes.Cmd.Cd_MovEje_MovToFza_Yield:
            param =  params.mov_to_fza_yield
        
        tx_header.set_data_len(param.get_bytes_size())

    return tx_header


class DataBuilder:
    
    def buid_sync_on_data(paso):
        param = AcdpMsgParams().sync_on
        setattr(param, 'paso_eje_lineal', paso)


    def build_yield_data(factor_limite_elastico, correccion_pendiente, cedencia):
        param = getattr(AcdpMsgParams(), 'yield')
        setattr(param, 'factor_limite_elastico', factor_limite_elastico)
        setattr(param, 'correccion_pendiente', correccion_pendiente)
        setattr(param, 'cedencia', cedencia)
        return param
    
    def build_mov_to_pos(ref, ref_rate):
        param = AcdpMsgParams().mov_to_pos
        param.reference = ref
        param.ref_rate = ref_rate
        return param

    def build_mov_to_pos_yield(ref, ref_rate, factor_limite_elastico, correccion_pendiente, cedencia):
        param = AcdpMsgParams().mov_to_pos_load_yield
        setattr(param, 'mov_to_pos', DataBuilder.build_mov_to_pos(ref, ref_rate))
        setattr(param, 'yield', DataBuilder.build_yield_data(factor_limite_elastico, correccion_pendiente, cedencia))
        return param

    def build_mov_to_pos_load(ref):
        param = AcdpMsgParams().mov_to_pos_load
        param.reference = ref
        return param

    def build_mov_to_pos_load_yield(ref, factor_limite_elastico, correccion_pendiente, cedencia):
        param = AcdpMsgParams().mov_to_pos_load_yield
        setattr(param, 'mov_to_pos_load', DataBuilder.build_mov_to_pos_load(ref))
        setattr(param, 'yield', DataBuilder.build_yield_data(factor_limite_elastico, correccion_pendiente, cedencia))
        return param

    def build_mov_to_fza_data(ref, ref_rate, vel_uns_max=0.0):        # REVISAR valor de vel_uns_max
        param = AcdpMsgParams().mov_to_fza
        setattr(param, 'reference', ref)
        setattr(param, 'ref_rate', ref_rate)
        setattr(param, 'vel_uns_max', vel_uns_max)
        return param

    def build_mov_to_fza_yield_data(ref, ref_rate, factor_limite_elastico, correccion_pendiente, cedencia, vel_uns_max=0.0):        # REVISAR valor de vel_uns_max
        param = AcdpMsgParams().mov_to_fza_yield
        setattr(param, 'mov_to_fza', DataBuilder.build_mov_to_fza_data(ref, ref_rate, vel_uns_max))
        setattr(param, 'yield', DataBuilder.build_yield_data(factor_limite_elastico, correccion_pendiente, cedencia))
        return param