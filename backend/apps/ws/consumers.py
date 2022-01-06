import json

from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.layers import get_channel_layer

from apps.ws.models import ChannelInfo
from apps.ws.utils.variables import MicroState


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
        else:
            MicroState.last_rx_header.store_from_raw(bytes_data)

    def micro_command(self, event):
        self.send(bytes_data=event['bytes_data'])

    def disconnect(self, close_code):
        print("DISCONNECED CODE: ", close_code)

        channel_info = ChannelInfo.objects.get(name=self.channel_name)
        channel_info.delete()

        self.close()
