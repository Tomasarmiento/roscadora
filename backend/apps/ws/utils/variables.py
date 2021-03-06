from datetime import datetime
from apps.service.acdp.acdp import AcdpHeader
from apps.service.acdp.messages_app import AcdpPc

class MicroState:
    # Comunications
    last_rx_header  = AcdpHeader()
    last_rx_data    = AcdpPc()
    msg_id          = 0         # Id of last msg sent
    cmd_rejected    = False
    cmd_ok          = False
    
    # Front
    log_messages    = []
    err_messages    = []

    # Remote/Local digital I/O
    rem_i_states        = []        # A dictionary with boolean values for each flag
    rem_o_states        = []
    rem_i               = []        # Int number with flags values
    rem_o               = []
    loc_i_states        = None
    loc_o_states        = None
    loc_i               = {}
    loc_o               = {}

    # Flags
    micro_flags     = {}            # Flags on the data part of the rx message
    axis_flags      = [{}, {}, {}]  # Indexes corresponds with axis index
    stopped         = False         # Raised when command/movemnt is interrupted
    stop_messages   = []            # Describes stop cause

    # Measurements
    axis_measures   = [{}, {}, {}]

    # Routines flags
    routine_stopped = False
    routine_ongoing = False
    load_allow_presure_off      = True
    roscado_allow_presure_off   = True

    # Master routine flags
    master_running      = False
    master_stop         = False
    end_master_routine  = False
    iteration           = 0

    # Graph
    position_values     = []
    torque_values       = []
    graph_flag          = True
    graph_duration      = 0

    # General
    load_on_timer       = datetime.now()    # Timer para apagar eje de carga con cabezal clampeado
    turn_on_timer       = datetime.now()    # Timer para apagar eje de husillo con velocidad 0
    turn_load_drv_off   = False
    turn_turn_drv_off   = False

class WsCodes:
    states          = 0
    cmd_ok          = 1
    cmd_rejected    = 2
    error_msg       = 3
    log_msg         = 4
    last_rx_header  = 5

front_channel_name = ''
back_channel_name = ''