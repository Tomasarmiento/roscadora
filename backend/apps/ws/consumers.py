import json

from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.layers import get_channel_layer

from apps.ws.models import ChannelInfo
from apps.ws.utils.variables import MicroState
from apps.ws.utils import variables as ws_vars

from apps.control.utils import variables as ctrl_vars
from apps.control.utils import functions as ctrl_fun

from apps.service.acdp import messages_base as msg_base
from apps.service.api.variables import Commands
from apps.service.acdp.handlers import build_msg


class FrontConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.set_channel_info()
        ws_vars.front_channel_name = self.channel_name
        print("FRONT WS CONNECTED")
        await self.accept()
    
    async def receive(self, text_data=None, bytes_data=None):
        print(text_data)
    
    async def disconnected(self, close_code):
        print("Front ws disconnected, code", close_code)
        await self.delete_channel_info()
        await self.close()
    
    async def front_message(self, event):
        await self.send(text_data=json.dumps(event['data']))
    
    @database_sync_to_async
    def set_channel_info(self):
        ChannelInfo.objects.create(
            source = 'front',
            name = self.channel_name
        )
    
    @database_sync_to_async
    def delete_channel_info(self):
        channel_info = ChannelInfo.objects.get(name=self.channel_name)
        channel_info.delete()

class MicroDataConsumer(WebsocketConsumer):

    def connect(self):
        ChannelInfo.objects.create(
            source='micro',
            name = self.channel_name,
            log = 0
            )
        ws_vars.back_channel_name = self.channel_name
        self.accept()
        print('Micro WS data connected')

    def receive(self, text_data=None, bytes_data=None):

        h_bytes_len = MicroState.last_rx_header.bytes_length
        if len(bytes_data) > h_bytes_len:
            MicroState.last_rx_header.store_from_raw(bytes_data[:h_bytes_len])
            MicroState.last_rx_data.store_from_raw(bytes_data[h_bytes_len:])
            ctrl_fun.update_states(micro_data=MicroState.last_rx_data)
            
            if MicroState.turn_load_drv_off:
                MicroState.turn_load_drv_off = False
                command = Commands.power_off
                axis = ctrl_vars.AXIS_IDS['carga']
                msg_id = ws_vars.MicroState.last_rx_header.get_msg_id() + 1
                ws_vars.MicroState.msg_id = msg_id
                header = build_msg(command, eje=axis, msg_id=msg_id)
                header = header.pacself()
                self.send(bytes_data=header)
            
            if MicroState.turn_turn_drv_off:
                MicroState.turn_turn_drv_off = False
                command = Commands.power_off
                axis = ctrl_vars.AXIS_IDS['giro']
                msg_id = ws_vars.MicroState.last_rx_header.get_msg_id() + 1
                ws_vars.MicroState.msg_id = msg_id
                header = build_msg(command, eje=axis, msg_id=msg_id)
                header = header.pacself()
                self.send(bytes_data=header)

            # show_states(MicroState.last_rx_header, MicroState.last_rx_data)
        else:
            MicroState.last_rx_header.store_from_raw(bytes_data)

    def micro_command(self, event):
        self.send(bytes_data=event['bytes_data'])

    def disconnect(self, close_code):
        print("DISCONNECED CODE: ", close_code)

        channel_info = ChannelInfo.objects.get(name=self.channel_name)
        channel_info.delete()

        self.close()


class MicroLogConsumer(WebsocketConsumer):

    def connect(self):
        ChannelInfo.objects.create(
            source='micro',
            name = self.channel_name,
            log = 1
            )
        ws_vars.back_channel_name = self.channel_name
        self.accept()
        print('Micro WS log connected')
    
    def receive(self, text_data=None, bytes_data=None):
        print(text_data)

    def micro_command(self, event):
        self.send(bytes_data=event['bytes_data'])

    def disconnect(self, close_code):
        print("DISCONNECED CODE: ", close_code)

        channel_info = ChannelInfo.objects.get(name=self.channel_name)
        channel_info.delete()

        self.close()


def show_states(header, data):
    print("-"*50)
    # for key, value in MicroState.rem_o_states[1].items():
    #     print(key, value)
    # print(ws_vars.MicroState.axis_flags[ctrl_var.AXIS_IDS['carga']]['drv_flags'] & msg_base.DrvFbkDataFlags.ENABLED)
    # print(ws_vars.MicroState.rem_o_states)
    # print(len(ws_vars.MicroState.position_values))
    # print(len(ws_vars.MicroState.torque_values))
    # print(ws_vars.MicroState.graph_duration)
    # print(ws_vars.MicroState.rem_i_states[1]['presion_normal'])
    for key, value in ws_vars.MicroState.loc_i.items():
        print(f'{key}:', f'{value:06b}')
    # print(ws_vars.MicroState.loc_i)
    # print (MicroState.axis_measures[ctrl_var.AXIS_IDS['carga']])
    # for axis in MicroState.axis_measures:
    #     print(axis)