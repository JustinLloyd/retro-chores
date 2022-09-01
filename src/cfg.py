import io

chore_display = None
toggle_switch_controller = None
vLEDStrip = None
chores = None
vfd = None

AVAILABLE_SLOTS = 12

pi = False
platform_confirmed = False
use_accelerated_time = True
use_fixed_start_time = True
emulated_hardware = True
real_hardware_available = False
clean_up_chores = False

def has_real_hardware():
    return real_hardware_available


def should_emulate_hardware():
    return emulated_hardware


def should_clean_up_chores():
    return clean_up_chores


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
