# from apps.service.acdp.acdp import AcdpHeader

class MicroState:
    msg_id          = 0
    cmd_rejected    = False
    cmd_ok          = True


class WsCodes:
    states          = 0
    cmd_ok          = 1
    cmd_rejected    = 2
    error_msg       = 3
    log_msg         = 4
    last_rx_header  = 5