import datetime
from time import sleep

from RPi import GPIO

from ctx import Ctx


def initialize():
    Ctx.DAY, Ctx.TIME = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S').split()
    Ctx.pwm.setPWMFreq(50)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Ctx.water_in_index, GPIO.OUT)
    GPIO.setup(Ctx.safety_index, GPIO.OUT)
    GPIO.setup(Ctx.water_out_index, GPIO.OUT)
    GPIO.setup(Ctx.air_index, GPIO.OUT)


def prepare():
    # pour food into fishfeeder
    for i in range(500, 1500, 20):
        Ctx.pwm.setServoPulse(Ctx.food_servo_index, i)
        sleep(0.02)

    for i in range(1500, 500, -20):
        Ctx.pwm.setServoPulse(Ctx.food_servo_index, i)
        sleep(0.02)
    # bring clean water to fishfeeder
    # GPIO.output(Ctx.water_in_index, GPIO.HIGH)
    # sleep(0.5)
    # GPIO.output(Ctx.water_in_index, GPIO.LOW)

    Ctx.STATUS = "FoodPrepared"


def stream():
    # stream water to fish tanks
    for _ in range(1):
        GPIO.output(Ctx.water_out_index, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(Ctx.water_out_index, GPIO.LOW)


def clean():
    for _ in range(2):
        # bring clean water to fishfeeder
        GPIO.output(Ctx.water_in_index, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(Ctx.water_in_index, GPIO.LOW)

        # thrash water from fishfeeder
        GPIO.output(Ctx.water_out_index, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(Ctx.water_out_index, GPIO.LOW)

    Ctx.STATUS = "Cleaned"


def finalize():
    GPIO.output(Ctx.water_in_index, GPIO.LOW)
    GPIO.output(Ctx.water_out_index, GPIO.LOW)
    GPIO.output(Ctx.air_index, GPIO.LOW)
    GPIO.output(Ctx.safety_index, GPIO.LOW)
    print Ctx.DAY, Ctx.TIME, Ctx.STATUS


# def run():
if __name__ == '__main__':
    # initialize ports
    initialize()
    print("initialized")

    # prepare food
    prepare()
    print("food prepared")

    # # deliver food to containers
    stream()
    print("food water mix streamed")
    #
    # # clean the tank
    # clean()

    # finalize
    finalize()
