from typing import io

pi = False
platform_confirmed = False


def is_raspberrypi():
    global platform_confirmed
    global pi
    if platform_confirmed:
        return pi

    try:
        platform_confirmed = True
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower():
                pi = True
                return True
    except Exception:
        pass
    return False
