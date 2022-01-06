import asyncio, json, struct, datetime
from collections import deque

from django.http import response
import websockets

from apps.service.acdp.acdp import ACDP_UDP_PORT, ACDP_IP_ADDR, AcdpHeader
from apps.service.acdp.handlers import AcdpMessage

from apps.service.api.functions import force_connection, open_connection, send_message

TIME_TO_SEC = 150 * 1000000
HOST = '127.0.0.1'
ACDP_IP = ACDP_IP_ADDR
PORT = ACDP_UDP_PORT
URI = "ws://localhost:8000/ws/micro/"


class Buffer():
    buffer = deque()
    add_to_buffer = False
    send_data = False
    reset_data = False

class UDPProtocol(asyncio.DatagramProtocol):
    transport = ''
    connected = False

    def __init__(self):
        super().__init__()
        self.rx_msg = AcdpMessage()

    def connection_made(self, transport):       # Used by asyncio
        self.transport = transport
        UDPProtocol.transport = transport
        UDPProtocol.connected = True
        force_connection(self.transport)
        
    def datagram_received(self, data, addr):    # addr is tuple (IP, PORT), example ('192.168.0.28', 54208)
        self.rx_msg.store_from_raw(data)
        WsStates.updata_front = self.rx_msg.process_rx_msg(transport=self.transport)
        
    def error_received(self, exc: Exception) -> None:
        return super().error_received(exc)

    def connection_lost(self, exc):     # exc: (self, exc: Optional[Exception]) -> None
        # ACDPMessage.connected = False
        UDPProtocol.connected = False
        return super().connection_lost(exc)


async def ws_graphs_client():
    uri = "ws://localhost:8000/ws/graphs/"
    while True:
        await asyncio.sleep(10)

async def ws_client():
    uri = "ws://localhost:8000/ws/micro/"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                await ws_handler(websocket)
                while websocket.open:
                    await asyncio.sleep(1)

        except ConnectionRefusedError:
            await asyncio.sleep(1)

        except KeyboardInterrupt:
            break


class WsStates:
    REFRESH_TIME = 0.01
    update_front = False
    micro_connected = False
    updata_front = False
    timestamp = 0


async def ws_handler(websocket):
    consumer_task = asyncio.ensure_future(ws_consumer(websocket))
    producer_task_1 = asyncio.ensure_future(ws_states_update(websocket))
    producer_task_2 = asyncio.ensure_future(ws_msg_response(websocket))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task_1, producer_task_2],
        return_when = asyncio.FIRST_COMPLETED
        )
    for task in pending:
        task.cancel()


async def ws_consumer(websocket):       # Fordwards message to micro. Message is already in bytes format
    while True:
        try:
            rx_msg = await websocket.recv()
        except websockets.exceptions.ConnectionClosed:
            break
        if UDPProtocol.connected:
            print("Sending msg")
            send_message(rx_msg, UDPProtocol.transport)


async def ws_states_update(websocket):
    while True:
        try:
            if WsStates.timestamp != AcdpMessage.last_rx_header.ctrl.timestamp:
                WsStates.timestamp = AcdpMessage.last_rx_header.ctrl.timestamp
                if WsStates.updata_front:
                    await websocket.send(AcdpMessage.last_rx_header.pacself())
                    WsStates.updata_front = False
            
            elif WsStates.micro_connected:
                print('ws_consumer - micro desconectado')
                WsStates.micro_connected = False
            
            await asyncio.sleep(WsStates.REFRESH_TIME)

        except websockets.exceptions.ConnectionClosed:
            break


async def ws_msg_response(websocket):
    while True:
        await asyncio.sleep(5)
        # try:
        #     while MicroWSHandler.pending_msg == False:
        #         await asyncio.sleep(0.01)
            
        #     MicroWSHandler.pending_msg = False
        #     msg = {
        #         "code": MicroWSHandler.code,
        #         "message": MicroWSHandler.message
        #     }

        #     await websocket.send(json.dumps(msg))

        # except websockets.exceptions.ConnectionClosed:
        #     break


def get_states_msg():
    return False
    # last_read = ACDPMessage.last_rx_data
    # last_rx_header = ACDPMessage.last_rx_header
    # micro_states = {}
    
    # # Measurementes
    # micro_states['v_pos'] = last_read.ctrl.eje.vertical.med.pos_fil
    # micro_states['v_vel'] = last_read.ctrl.eje.vertical.med.vel_fil
    # micro_states['v_fza'] = last_read.ctrl.eje.vertical.med.fza_fil
    # micro_states['v_strain'] = last_read.ctrl.eje.vertical.med.strain_fil
    # micro_states['h_pos'] = last_read.ctrl.eje.horizontal.med.pos_fil
    # micro_states['h_vel'] = last_read.ctrl.eje.horizontal.med.vel_fil
    # micro_states['cedencia'] = last_read.ctrl.eje.vertical.med.cedencia
    
    # # States
    # micro_states['states'] = last_read.get_state_flags()
    # micro_states['start_scan'] = micro_states['states']['ctrl']['flags'] & ACDPDataEnums.FLG_DIG_INPUT_INICIAR_ENDEREZADO.value
    # micro_states['unknown_zero_v'] = last_read.ctrl.eje.vertical.med.drv_fbk.flags & DrviverFlags.ACDP_FLAGSTAT_DrvFbk_UnknownZero.value
    # micro_states['unknown_zero_h'] = last_read.ctrl.eje.horizontal.med.drv_fbk.flags & DrviverFlags.ACDP_FLAGSTAT_DrvFbk_UnknownZero.value

    # # Connection
    # micro_states['channel'] = last_rx_header.cxn_channel
    # micro_states['msg_code'] = last_rx_header.ctrl.msg_code

    # msg = {
    #     "code": WS_CODES['states'],
    #     "states": micro_states
    # }
    # return msg


async def close_con(transport):     # close (udp) connection
    await asyncio.sleep(1)
    print('CLOSE CONNECTION')
    # send_header = build_header(COMMANDS['close_connection'], host_ip=HOST, dest_ip=ACDP_IP)
    # transport.sendto(send_header.pack_self(), (ACDP_IP, PORT))
    transport.close()