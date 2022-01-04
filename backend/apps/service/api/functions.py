from apps.service.acdp.messages_app import AcdpAxisMovementEnums, AcdpMsgCodes
from apps.service.acdp.handlers import build_header
from apps.service.acdp.acdp import ACDP_UDP_PORT, ACDP_IP_ADDR
from .variables import COMMANDS, Commands, last_rx_msg

def send_message(bytes_msg, transport, addr=(ACDP_IP_ADDR, ACDP_UDP_PORT)):
    if transport:
        transport.sendto(bytes_msg, addr)
    else:
        print("Sin conexion")


def open_connection(transport):
    header = build_header(Commands.open_connection)
    send_message(header.pacself(), transport)


def force_connection(transport):
    header = build_header(Commands.force_connection)
    send_message(header.pacself(), transport)


def close_connection(transport):
    header = build_header(Commands.close_connection)
    send_message(header.pacself(), transport)


def stop(transport):
    msg_id = last_rx_msg.get_msg_id() + 1
    header = build_header(Commands.stop, msg_id = msg_id)
    send_message(header.pacself(), transport)

def echo_reply(transport):
    msg_id = last_rx_msg.get_msg_id() + 1
    header = build_header(Commands.echo_reply, msg_id = msg_id)
    send_message(header.pacself(), transport)


def sync_on(transport, paso):
    msg_id = last_rx_msg.get_msg_id() + 1
    header = build_header(Commands.echo_reply, msg_id = msg_id, paso=paso)
    send_message(header.pacself(), transport)


# Cd_MovEje_SyncOn             = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x05  # Parametro: Param::tSyncOn
# Cd_MovEje_SyncOff            = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x06
# Cd_MovEje_RunZeroing         = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x07
# Cd_MovEje_RunPositioning     = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x08
# Cd_MovEje_MovToVel           = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x09  # Parametro: Param::tMovToVel
# Cd_MovEje_SetRefVel          = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x0a  # Parametro: Param::tSetRefVel
# Cd_MovEje_MovToPos           = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x0b  # Parametro: Param::tMovToPos
# Cd_MovEje_SetRefPos          = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x0c  # Parametro: Param::tSetRefPos
# Cd_MovEje_MovToPos_Yield     = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x0d  # Parametro: Param::tMovToPos_Yield
# Cd_MovEje_MovToPosLoad       = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x0e  # Parametro: Param::tMovToPosLoad
# Cd_MovEje_SetRefPosLoad      = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x0f  # Parametro: Param::tSetRefPosLoad
# Cd_MovEje_MovToPosLoad_Yield = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x10  # Parametro: Param::tMovToPosLoad_Yield
# Cd_MovEje_MovToFza           = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x11  # Parametro: Param::tMovToFza
# Cd_MovEje_SetRefFza          = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x12  # Parametro: Param::tSetRefFza
# Cd_MovEje_MovToFza_Yield     = AcdpMsgType.CMD + AcdpMsgLevel.APPLICATION + 0x13  # Parametro: Param::tMovToFza_Yield