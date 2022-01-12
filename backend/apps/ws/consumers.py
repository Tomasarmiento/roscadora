import json

from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.layers import get_channel_layer

from apps.ws.models import ChannelInfo
from apps.ws.utils.variables import MicroState
from apps.ws.utils import variables as ws_vars
from apps.control.utils import variables as ctrl_var
from apps.control.utils import functions as ctrl_fun


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

class MicroConsumer(WebsocketConsumer):

    def connect(self):
        ChannelInfo.objects.create(
            source='micro',
            name = self.channel_name
            )
        ws_vars.back_channel_name = self.channel_name
        self.accept()
        print('Micro WS connected')

    def receive(self, text_data=None, bytes_data=None):
        h_bytes_len = MicroState.last_rx_header.bytes_length
        if len(bytes_data) > h_bytes_len:
            MicroState.last_rx_header.store_from_raw(bytes_data[:h_bytes_len])
            MicroState.last_rx_data.store_from_raw(bytes_data[h_bytes_len:])
            ctrl_fun.update_states(micro_data=MicroState.last_rx_data)
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


def show_states(header, data):
    print("-"*50)
    # for key, value in MicroState.rem_o_states[1].items():
    #     print(key, value)
    print (MicroState.axis_flags[ctrl_var.AXIS_IDS['giro']]['estado'])
    # for axis in MicroState.axis_measures:
    #     print(axis)