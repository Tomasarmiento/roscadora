from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_message(header, ch_info, msg=None):
    
    ws_data = b''

    if msg:
        ws_data = msg.pacself()
    else:
        ws_data = header.pacself()
    
    try:
        ch_layer = get_channel_layer()
        payload = {
            'type': 'micro.command',
            'bytes_data': ws_data
        }
        async_to_sync(ch_layer.send)(
            ch_info.name,
            payload
        )
    
    except ch_info.DoesNotExist:
        print("Micro not connected")