from apps.service.acdp.messages_base import AcdpMsgCxn
from apps.service.acdp.messages_app import AcdpMsgCodes
from apps.service.acdp.handlers import AcdpMessage


# -------------------------------------------------------------------------------------------- #
# ------------------------------------- Constants -------------------------------------------- #
# -------------------------------------------------------------------------------------------- #

class Commands:
    power_on = AcdpMsgCodes.Cmd.Cd_MovEje_PowerOn,
    power_off = AcdpMsgCodes.Cmd.Cd_MovEje_PowerOff,

    # Connection
    open_connection = AcdpMsgCxn.CD_CONNECT,
    force_connection = AcdpMsgCxn.CD_FORCE_CONNECT,
    close_connection = AcdpMsgCxn.CD_DISCONNECT,
    connection_stat = AcdpMsgCxn.CD_CONNECTION_STAT,

    echo_reply = AcdpMsgCxn.CD_ECHO_REPLY,

    # Axis
    stop = AcdpMsgCodes.Cmd.Cd_MovEje_Stop,
    fast_stop = AcdpMsgCodes.Cmd.Cd_MovEje_FastStop,

    run_zeroing = AcdpMsgCodes.Cmd.Cd_MovEje_RunZeroing,
    run_positioning = AcdpMsgCodes.Cmd.Cd_MovEje_RunPositioning,

    mov_to_vel = AcdpMsgCodes.Cmd.Cd_MovEje_MovToVel,
    mov_to_pos_yield = AcdpMsgCodes.Cmd.Cd_MovEje_MovToPos_Yield,
    mov_to_pos_load = AcdpMsgCodes.Cmd.Cd_MovEje_MovToPosLoad,
    mov_to_pos_load_yield = AcdpMsgCodes.Cmd.Cd_MovEje_MovToPosLoad_Yield,
    mov_to_fza = AcdpMsgCodes.Cmd.Cd_MovEje_MovToFza,
    mov_to_fza_yield = AcdpMsgCodes.Cmd.Cd_MovEje_MovToFza_Yield,

    # Set refs
    set_ref_pos = AcdpMsgCodes.Cmd.Cd_MovEje_SetRefPos,
    set_ref_vel = AcdpMsgCodes.Cmd.Cd_MovEje_SetRefVel,
    set_ref_pos_load = AcdpMsgCodes.Cmd.Cd_MovEje_SetRefPosLoad,
    set_ref_fza = AcdpMsgCodes.Cmd.Cd_MovEje_SetRefFza,

    #Sync
    sync_on = AcdpMsgCodes.Cmd.Cd_MovEje_SyncOn,        # Se usa para sincronizar el movimiento del eje lineal con el de rotacion
                                                        # Se manda sync on antes de empezar el movimiento y se setea el paso. Despues solo se comanda el lineal
    sync_off = AcdpMsgCodes.Cmd.Cd_MovEje_SyncOff,

    # IO
    loc_do_set = AcdpMsgCodes.Cmd.Cd_LocDO_Set,
    rem_do_set = AcdpMsgCodes.Cmd.Cd_RemDO_Set

COMMANDS = {
    'power_on': AcdpMsgCodes.Cmd.Cd_MovEje_PowerOn,
    'power_off': AcdpMsgCodes.Cmd.Cd_MovEje_PowerOff,

    # Connection
    'open_connection': AcdpMsgCxn.CD_CONNECT,
    'force_connection': AcdpMsgCxn.CD_FORCE_CONNECT,
    'close_connection': AcdpMsgCxn.CD_DISCONNECT,
    'connection_stat': AcdpMsgCxn.CD_CONNECTION_STAT,

    'echo_reply': AcdpMsgCxn.CD_ECHO_REPLY,

    # Axis
    'stop': AcdpMsgCodes.Cmd.Cd_MovEje_Stop,
    'fast_stop': AcdpMsgCodes.Cmd.Cd_MovEje_FastStop,

    'run_zeroing': AcdpMsgCodes.Cmd.Cd_MovEje_RunZeroing,
    'run_positioning': AcdpMsgCodes.Cmd.Cd_MovEje_RunPositioning,

    'mov_to_vel': AcdpMsgCodes.Cmd.Cd_MovEje_MovToVel,
    'mov_to_pos': AcdpMsgCodes.Cmd.Cd_MovEje_MovToPos,
    'mov_to_pos_yield': AcdpMsgCodes.Cmd.Cd_MovEje_MovToPos_Yield,
    'mov_to_pos_load': AcdpMsgCodes.Cmd.Cd_MovEje_MovToPosLoad,
    'mov_to_pos_load_yield': AcdpMsgCodes.Cmd.Cd_MovEje_MovToPosLoad_Yield,
    'mov_to_fza': AcdpMsgCodes.Cmd.Cd_MovEje_MovToFza,
    'mov_to_fza_yield': AcdpMsgCodes.Cmd.Cd_MovEje_MovToFza_Yield,

    # Set refs
    'set_ref_pos': AcdpMsgCodes.Cmd.Cd_MovEje_SetRefPos,
    'set_ref_vel': AcdpMsgCodes.Cmd.Cd_MovEje_SetRefVel,
    'set_ref_pos_load': AcdpMsgCodes.Cmd.Cd_MovEje_SetRefPosLoad,
    'set_ref_fza': AcdpMsgCodes.Cmd.Cd_MovEje_SetRefFza,

    #Sync
    'sync_on': AcdpMsgCodes.Cmd.Cd_MovEje_SyncOn,       # Se usa para sincronizar el movimiento del eje lineal con el de rotacion
                                                        # Se manda sync on antes de empezar el movimiento y se setea el paso. Despues solo se comanda el lineal
    'sync_off': AcdpMsgCodes.Cmd.Cd_MovEje_SyncOff,

    # Loc/Rem I/O
    'loc_do_set': AcdpMsgCodes.Cmd.Cd_LocDO_Set,
    'rem_do_set': AcdpMsgCodes.Cmd.Cd_RemDO_Set
}


# -------------------------------------------------------------------------------------------- #
# ------------------------------------- Variables -------------------------------------------- #
# -------------------------------------------------------------------------------------------- #

last_rx_msg = AcdpMessage()