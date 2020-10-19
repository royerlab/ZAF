from time import sleep

from RPi import GPIO

from python.zaf2.control_box import ControlBox


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Context(object):
    __metaclass__ = Singleton

    food_servo = 5

    water_out1 = 4
    water_out2 = 3
    water_in = 2

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
        cls.control_box.initialize()

    @classmethod
    def check_water_sensor(cls):
        if GPIO.input(cls.water_sensor) == GPIO.LOW:
            print("no water warning by sensor")
            cls.control_box.set_pwm(cls.safety_pump, 0)
        else:
            print("WATER WARNING by sensor")
            cls.control_box.set_pwm(cls.safety_pump, 255)

    @classmethod
    def run_pump(cls, pumps, duration=0.5):
        for pump in pumps:
            cls.control_box.set_pwm(pump, 255)

        sleep(duration)

        for pump in pumps:
            cls.control_box.set_pwm(pump, 0)

    @classmethod
    def rotate_food_servo(cls, angle):
        if angle < 0 or angle > 180:
            raise ValueError("angle argument has to be between 0, 180")

        cls.control_box.set_pwm(cls.food_servo, angle)
        sleep(0.02)
