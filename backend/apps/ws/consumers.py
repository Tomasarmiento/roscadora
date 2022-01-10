import json

from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.layers import get_channel_layer

from apps.ws.models import ChannelInfo
from apps.ws.utils.variables import MicroState
from apps.control.utils import variables as ctrl_var
from apps.control.utils import functions as ctrl_fun


class MicroConsumer(WebsocketConsumer):

    def connect(self):
        ChannelInfo.objects.create(
            source='micro',
            name = self.channel_name
            )
        self.accept()
        print('Micro WS connected')

    def receive(self, text_data=None, bytes_data=None):
        h_bytes_len = MicroState.last_rx_header.bytes_length
        if len(bytes_data) > h_bytes_len:
            MicroState.last_rx_header.store_from_raw(bytes_data[:h_bytes_len])
            MicroState.last_rx_data.store_from_raw(bytes_data[h_bytes_len:])
            ctrl_fun.update_states(micro_data=MicroState.last_rx_data)
            show_states(MicroState.last_rx_header, MicroState.last_rx_data)
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
    # print("-"*50,)
    # print('REM IO:', data.data.ctrl.rem_io.di16[0])
    # for key, val in MicroState.rem_o_states[0].items():
    #     print(key, val)
    # for axis in MicroState.axis_flags:
    #     print("-"*50)
    #     print(axis)
    # print("\n", "-"*20, "AVANCE", "-"*20)
    # print(MicroState.eje_avance)
    # print("\n", "-"*20, "CARGA", "-"*20)
    # print(MicroState.eje_carga)
    print("\n", "-"*20, "GIRO", "-"*20)
    print(MicroState.eje_giro)