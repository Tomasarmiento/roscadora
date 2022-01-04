def init_channel_info(ch_model):
    chs = ch_model.objects.filter(source='front')
    for ch in chs:
        ch.delete()
    
    chs = ch_model.objects.filter(source='micro')
    for ch in chs:
        ch.delete()