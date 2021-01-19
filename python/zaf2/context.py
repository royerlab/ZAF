from time import sleep
from RPi import GPIO
from arbol.arbol import lprint

from python.zaf2.control_box import ControlBox


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Context(object):
    __metaclass__ = Singleton

    early_stop = False

    food_servo = 5

    water_out1 = 0
    water_out2 = 3
    water_in = 6

    air_pump = 1
    safety_pump = 0

    # This will be GPIO BCM
    water_sensor = 14

    DAY = None
    TIME = None
    STATUS = None

    control_box = ControlBox()

    @classmethod
    def initialize(cls):
        if cls.early_stop:
            exit(1)
        else:
            cls.control_box.initialize()

    @classmethod
    def check_water_sensor(cls):
        if cls.early_stop:
            exit(1)
        else:
            if GPIO.input(cls.water_sensor) == GPIO.LOW:
                lprint("no water warning by sensor")
                cls.control_box.set_pwm(cls.safety_pump, 0)
            else:
                lprint("WATER WARNING by sensor")
                cls.control_box.set_pwm(cls.safety_pump, 255)

    @classmethod
    def run_pump(cls, index, duration=1):
        if cls.early_stop:
            exit(1)
        else:
            cls.control_box.set_pwm(index, 255)
            sleep(duration)
            cls.control_box.set_pwm(index, 0)

    @classmethod
    def rotate_food_servo(cls, angle):
        if cls.early_stop:
            exit(1)
        else:
            if angle < 0 or angle > 180:
                raise ValueError("angle argument has to be between 0, 180")

            cls.control_box.set_pwm(cls.food_servo, angle)
            sleep(1)
