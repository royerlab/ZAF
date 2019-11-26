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

    # These are servo hat indices
    water_out1 = 13
    water_out2 = 12

    water_in = 9
    water_in_valve = 8

    air_pump = 5
    safety_pump = 4

    food_servo_index = 0

    # This will be GPIO BCM
    water_sensor = 14  # not connected to GPIO yet
