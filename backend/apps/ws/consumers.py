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
    print("-"*50,)
    # print('REM IO:', data.data.ctrl.rem_io.di16[0])
    # for key, val in MicroState.micro_flags.items():
    #     print(key, val)
    for i in range(3):
        axis = data.get_states()['axis'][i]
        # print(axis.get_values())
        print(
            # 'Flags:', axis['flags'],
            # '\nFlags fin de estado:', axis['flags_fin'],
            # '\nMaquina de estados:', axis['state'],
            # '\nHoming states:', axis['pos_homing_states'],
            '\nPosicion:', axis['pos_fil'],
            '\nVelocidad:', axis['vel_fil'],
            # '\nPos carga:', axis['load_pos_fil'],
            # '\nVel carga:', axis['load_vel_fil'],
            # '\nRem do:', data.rem_do,
            # '\nRem_di', data.rem_di
        )