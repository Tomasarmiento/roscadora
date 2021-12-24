import asyncio
import json
from collections import deque

from django.http import response
import websockets

# from apps.service.acdp.handlers import send_command, process_rx_message, build_header
# from apps.service.acdp.handlers import IPAddress, ACDPMessage, MicroWSHandler
# from apps.service.acdp.commands import WS_CODES, COMMANDS, ROUTINE_COMMANDS
# from apps.service.acdp.messages import ACDPDataEnums
# from apps.service.acdp.messages_base import DrviverFlags
from apps.service.acdp.acdp import ACDP_UDP_PORT
from apps.service.acdp.handlers import AcdpMessage

TIME_TO_SEC = 150 * 1000000
HOST = '127.0.0.1'
ACDP_IP = '192.168.0.101'
PORT = ACDP_UDP_PORT
URI = "ws://localhost:8000/ws/micro/"
HOR_GRAPH_STEP = 0.1
REFRESH_TIME = 0.1          # Time to refresh states on frontend in seconds


class Buffer():
    buffer = deque()
    add_to_buffer = False
    send_data = False
    reset_data = False

class UDPProtocol(asyncio.DatagramProtocol):
    transport = ''

    def __init__(self):
        super().__init__()

    def connection_made(self, transport):       # Used by asyncio
        self.transport = transport
        UDPProtocol.transport = transport
        # send_header = build_header(COMMANDS['connect'], host_ip=HOST, dest_ip=ACDP_IP)
        # self.transport.sendto(send_header.pack_self(),(ACDP_IP, PORT))
        
    def datagram_received(self, data, addr):    # addr is tuple (IP, PORT), example ('192.168.0.28', 54208)
        rx_msg = AcdpMessage()
        rx_msg.store_from_raw(data)
        # if not MicroWSHandler.micro_connected:
        #     MicroWSHandler.micro_connected = True
        #     MicroWSHandler.code = WS_CODES['connected']
        #     MicroWSHandler.pending_msg = True
        
        # process_rx_message(
        #     transport = self.transport,
        #     rx_message = data,
        #     HOST = HOST,
        #     addr = addr,
        #     buffer = Buffer
        #     )

    def error_received(self, exc: Exception) -> None:
        return super().error_received(exc)

    def connection_lost(self, exc):     # exc: (self, exc: Optional[Exception]) -> None
        # ACDPMessage.connected = False
        return super().connection_lost(exc)


async def ws_data_client():
    uri = "ws://localhost:8000/ws/graphs/"
    while True:
        await asyncio.sleep(10)
    #     try:
    #         async with websockets.connect(uri) as websocket:
    #             while websocket.open:

    #                 while not Buffer.send_data and not Buffer.reset_data:
    #                     await asyncio.sleep(0.5)

    #                 msg = {}
                    
    #                 if Buffer.send_data:
    #                     msg = {
    #                         'data_start': True
    #                     }
    #                     await websocket.send(json.dumps(msg))
    #                     msg = {}
    #                     # await asyncio.sleep(0.1)
    #                     while Buffer.send_data:
    #                         while Buffer.buffer:
    #                             val = Buffer.buffer.popleft()
    #                             msg['v_pos'] = val.ctrl.eje.vertical.med.pos_fil
    #                             msg['v_vel'] = val.ctrl.eje.vertical.med.vel_fil
    #                             msg['v_fza'] = val.ctrl.eje.vertical.med.fza_fil
    #                             msg['v_strain'] = val.ctrl.eje.vertical.med.strain_fil
    #                             msg['v_strain_rate'] = val.ctrl.eje.vertical.med.strain_rate_fil
    #                             msg['v_yield'] = val.ctrl.eje.vertical.med.rigidez_probeta
    #                             msg['h_pos'] = val.ctrl.eje.horizontal.med.pos_fil
    #                             msg['h_vel'] = val.ctrl.eje.horizontal.med.vel_fil
    #                             msg['cedencia'] = val.ctrl.eje.vertical.med.cedencia
    #                             await websocket.send(json.dumps(msg))
    #                         await asyncio.sleep(0.001)
    #                     msg = {'data_end': True}
    #                     await websocket.send(json.dumps(msg))
    #                     # Buffer.send_data = False
    #                     Buffer.buffer.clear()
                    
    #                 elif Buffer.reset_data:
    #                     Buffer.reset_data = False
    #                     msg = {
    #                         'data_reset': True
    #                     }
    #                     await websocket.send(json.dumps(msg))
        
    #     except ConnectionRefusedError:
    #         # print('CONNECTION REFUSED (SERVICE)')
    #         await asyncio.sleep(2)

async def ws_client():
    uri = "ws://localhost:8000/ws/micro/"
    while True:
        await asyncio.sleep(10)
    #     try:
    #         async with websockets.connect(uri) as websocket:
    #             await ws_handler(websocket)
    #             while websocket.open:
    #                 await asyncio.sleep(1)

    #     except ConnectionRefusedError:
    #         # print('CONNECTION REFUSED (SERVICE)')
    #         await asyncio.sleep(1)


async def ws_handler(ws):
    consumer_task = asyncio.ensure_future(ws_consumer(ws))
    producer_task_1 = asyncio.ensure_future(ws_states_update(ws))
    producer_task_2 = asyncio.ensure_future(ws_msg_response(ws))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task_1, producer_task_2],
        return_when = asyncio.FIRST_COMPLETED
        )
    for task in pending:
        task.cancel()


async def ws_states_update(websocket):
    while True:
        await asyncio.sleep(10)
        # try:
        #     if MicroWSHandler.timestamp != ACDPMessage.last_rx_header.ctrl.timestamp:
        #         MicroWSHandler.timestamp = ACDPMessage.last_rx_header.ctrl.timestamp
        #         msg = get_states_msg()
        #         await websocket.send(json.dumps(msg))
            
        #     elif MicroWSHandler.micro_connected:
        #         print('ws_consumer - micro desconectado')
        #         MicroWSHandler.micro_connected = False
        #         MicroWSHandler.code = WS_CODES['disconnected']
        #         MicroWSHandler.pending_msg = True
            
        #     await asyncio.sleep(REFRESH_TIME)

        # except websockets.exceptions.ConnectionClosed:
        #     break


async def ws_consumer(websocket):
    while True:
        await asyncio.sleep(10)
        # try:
        #     rx_msg = await websocket.recv()
        # except websockets.exceptions.ConnectionClosed:
        #     break
        # rx_msg = json.loads(rx_msg)
        # rx_command = int(rx_msg['command'])
        
        # if MicroWSHandler.micro_connected:
            
        #     if rx_command in COMMANDS.values() or rx_command in ROUTINE_COMMANDS.values():
                
        #         if rx_command != COMMANDS['monitor']:
        #             print('Comando valido PROTOCOLS: ', rx_command)
        #             print('RX CMD PROTOCOLS: ', rx_command)
        #             print('RX MSG PROTOCOLS: ', rx_msg)
        #             MicroWSHandler.wait_ok = True

        #         transport = UDPProtocol.transport
        #         response = send_command(message=rx_msg, transport=transport)

        #         if response:    # only for monitor command
        #             msg = {
        #                 "code": WS_CODES['states'],
        #                 "states": response
        #             }
        #             await websocket.send(json.dumps(msg))

        #         if rx_command in ROUTINE_COMMANDS.values():
        #             if rx_command == ROUTINE_COMMANDS['start_data_adq']:
        #                 Buffer.buffer.clear()
        #                 Buffer.add_to_buffer = True
        #                 Buffer.send_data = True
                    
        #             if rx_command == ROUTINE_COMMANDS['stop_data_adq']:
        #                 Buffer.add_to_buffer = False
        #                 Buffer.send_data = False
                    
        #             if rx_command == ROUTINE_COMMANDS['reset_data_adq']:
        #                 Buffer.add_to_buffer = False
        #                 Buffer.send_data = False
        #                 Buffer.buffer.clear()
        #                 Buffer.reset_data = True
        
        # elif rx_command == COMMANDS['connect']:
        #     transport = UDPProtocol.transport
        #     send_header = build_header(COMMANDS['connect'], host_ip=HOST, dest_ip=ACDP_IP)
        #     transport.sendto(send_header.pack_self(),(ACDP_IP, PORT))
        
        # else:
        #     MicroWSHandler.code = WS_CODES['disconnected']
        #     MicroWSHandler.pending_msg = True


async def ws_msg_response(websocket):
    while True:
        try:
            while MicroWSHandler.pending_msg == False:
                await asyncio.sleep(0.01)
            
            MicroWSHandler.pending_msg = False
            msg = {
                "code": MicroWSHandler.code,
                "message": MicroWSHandler.message
            }

            await websocket.send(json.dumps(msg))

        except websockets.exceptions.ConnectionClosed:
            break


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