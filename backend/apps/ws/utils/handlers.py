from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_message(header, ch_info, data=None):        # Converts msg to bytes and sends it to ws micro connection
    
    msg = header.pacself()

    if data:
        msg += data.pacself()
    
    try:
        ch_layer = get_channel_layer()
        payload = {
            'type': 'micro.command',
            'bytes_data': msg
        }
        async_to_sync(ch_layer.send)(
            ch_info.name,
            payload
        )
    
    except ch_info.DoesNotExist:
        print("Micro not connected")