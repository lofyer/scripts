import random
def gen_mac(prefix='AC:DE:48'):
    return '{0}:{1:02X}:{2:02X}:{3:02X}'.format(prefix,
        random.randint(0, 0xff),
        random.randint(0, 0xff),
        random.randint(0, 0xff))
    
print gen_mac()
