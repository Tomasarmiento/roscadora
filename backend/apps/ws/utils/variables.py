from apps.service.acdp.acdp import AcdpHeader
from apps.service.acdp.messages_app import AcdpPc

class MicroState:
    msg_id          = 0
    cmd_rejected    = False
    cmd_ok          = True
    last_rx_header  = AcdpHeader()
    last_rx_data    = AcdpPc()


class WsCodes:
    states          = 0
    cmd_ok          = 1
    cmd_rejected    = 2
    error_msg       = 3
    log_msg         = 4
    last_rx_header  = 5