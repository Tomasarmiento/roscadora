from apps.service.acdp.handlers import build_header
from apps.service.acdp.acdp import ACDP_UDP_PORT, ACDP_IP_ADDR
from .constants import COMMANDS

def send_message(bytes_msg, transport, addr=(ACDP_IP_ADDR, ACDP_UDP_PORT)):
    if transport:
        transport.sendto(bytes_msg, addr)
    else:
        print("Sin conexion")

def open_connection(transport):
    header = build_header(COMMANDS['open_connection'])
    send_message(header.pacself(), transport)


def close_connection(transport):
    header = build_header(COMMANDS['close_connection'])
    send_message(header.pacself(), transport)