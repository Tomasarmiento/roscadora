from apps.service.acdp.acdp import AcdpHeader
from apps.service.acdp.messages_app import AcdpPc

class MicroState:
    # Comunications
    last_rx_header  = AcdpHeader()
    last_rx_data    = AcdpPc()
    msg_id          = 0         # Id of last msg sent
    cmd_rejected    = False
    cmd_ok          = True

    # Remote/Local digital I/O
    rem_i_states    = []
    rem_o_states    = []
    rem_i           = []
    rem_o           = []
    loc_i_states    = None
    loc_o_states    = None
    loc_i           = None
    loc_o           = None

    # Flags
    micro_flags     = {}            # Flags on the data part of the rx message
    axis_flags      = [{}, {}, {}]  # Indexes corresponds with Axis index


class WsCodes:
    states          = 0
    cmd_ok          = 1
    cmd_rejected    = 2
    error_msg       = 3
    log_msg         = 4
    last_rx_header  = 5