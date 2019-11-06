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

    water_out1_high = 21
    water_out1_low = 26  # random value for now

    water_out2_high = 20
    water_out2_low = 19  # random value for now

    water_in_high = 16
    water_in_low = 13

    air_pump_high = 19
    air_pump_low = 5

    safety_pump_high = 12
    safety_pump_low = 9

    water_sensor = 14
