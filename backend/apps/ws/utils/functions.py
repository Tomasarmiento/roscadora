def init_channel_info(ch_model):
    chs = ch_model.objects.filter(source='front')
    for ch in chs:
        ch.delete()
    
    chs = ch_model.objects.filter(source='micro')
    for ch in chs:
        ch.delete()


def get_ch_info(ch_model, source):
    try:
        return ch_model.objects.get(source=source)
    
    except ch_model.DoesNotExist:
        return False