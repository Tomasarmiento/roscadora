from .acdp import ACDP_VERSION, ACDP_UDP_PORT, ACDP_IP_ADDR
from .acdp import AcdpHeader
from .messages_app import AcdpPc, AcdpMsgCodes
from .messages_base import BaseStructure, AcdpMsgCxn

class AcdpMessage(BaseStructure):
    last_rx_data = AcdpPc()
    last_rx_header = AcdpHeader()

    _fields_ = [
        ('header', AcdpHeader),
        ('data', AcdpPc)
    ]

    def get_msg_id(self):
        return self.header.ctrl.msg_id


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
    
    elif code == AcdpMsgCodes.Cmd.Cd_MovEje_Stop:
        tx_header.set_msg_id(msg_id=kwargs['msg_id'])

    return tx_header


def process_rx_msg(rx_msg, addr=('192.168.0.100', ACDP_IP_ADDR), transport=None):
    msg_code = rx_msg.header.get_msg_code
    
    if msg_code == AcdpMsgCxn.CD_ECHO_REQ:
        print("ECHO REQ")
        tx_header = build_header(AcdpMsgCxn.CD_ECHO_REPLY)
        transport.sendto(tx_header.pacself(), addr)
        