from apps.service.acdp.messages_app import AcdpAxisMovementEnums
from apps.service.acdp.handlers import build_header
from apps.service.acdp.acdp import ACDP_UDP_PORT, ACDP_IP_ADDR
from .variables import COMMANDS, last_rx_msg

def send_message(bytes_msg, transport, addr=(ACDP_IP_ADDR, ACDP_UDP_PORT)):
    if transport:
        transport.sendto(bytes_msg, addr)
    else:
        print("Sin conexion")


def open_connection(transport):
    header = build_header(COMMANDS['open_connection'])
    send_message(header.pacself(), transport)


def force_connection(transport):
    header = build_header(COMMANDS['force_connection'])
    send_message(header.pacself(), transport)


def close_connection(transport):
    header = build_header(COMMANDS['close_connection'])
    send_message(header.pacself(), transport)


def stop(transport):
    msg_id = last_rx_msg.get_msg_id() + 1
    header = build_header(COMMANDS['stop'], msg_id = msg_id)
    send_message(header.pacself(), transport)

def echo_reply(transport):
    msg_id = last_rx_msg.get_msg_id() + 1
    header = build_header(COMMANDS['echo_reply'], msg_id = msg_id)
    send_message(header.pacself(), transport)