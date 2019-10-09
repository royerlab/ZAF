from picamera import PiCamera

from PCA9685 import PCA9685


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Ctx(object):
    __metaclass__ = Singleton
    # camera = PiCamera()
    pwm = PCA9685(0x40, debug=False)

    DAY = None
    TIME = None
    STATUS = None

    # this is not GPIO pin
    food_servo_index = 9
    # These are GPIO
    water_out_index = 21
    water_in_index = 20
    air_index = 19
    safety_index = 2
