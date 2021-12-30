from .acdp import ACDP_VERSION, ACDP_UDP_PORT, ACDP_IP_ADDR
from .acdp import AcdpHeader
from .messages_app import AcdpPc
from .messages_base import BaseStructure, AcdpMsgCxn

class AcdpMessage(BaseStructure):
    last_rx_data = AcdpPc()
    last_rx_header = AcdpHeader()

    _fields_ = [
        ('header', AcdpHeader),
        ('data', AcdpPc)
    ]


def build_header(command, host_ip="192.168.0.100", dest_ip=ACDP_IP_ADDR, *args, **kwargs):
    tx_header = AcdpHeader()
    tx_header.version = ACDP_VERSION
    tx_header.channel = 0
    tx_header.ip_addr.store_from_string(host_ip)
    tx_header.dest_addr.store_from_string(dest_ip)

    tx_header.ctrl.device_type = 0
    tx_header.ctrl.firmware_version = 0
    tx_header.ctrl.object = 0
    tx_header.ctrl.flags = 0
    tx_header.ctrl.msg_id = 0
    tx_header.ctrl.timestamp = 0
    tx_header.ctrl.data_len8 = 0

    if command == 'open_com':
        tx_header.ctrl.msg_code = AcdpMsgCxn.CD_FORCE_CONNECT
    
    return tx_header