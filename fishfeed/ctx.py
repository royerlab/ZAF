from picamera import PiCamera


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Ctx(object):
    __metaclass__ = Singleton
    # camera = PiCamera()
    pwm = None

    DAY = None
    TIME = None
    STATUS = None

    # These are GPIO - BCM
    food_servo_index = 17
    water_out_index = 21
    water_in_index = 20
    air_index = 19
    safety_index = 27
