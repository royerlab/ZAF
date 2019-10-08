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
    # put food
    for i in range(500, 1500, 20):
        Ctx.pwm.setServoPulse(Ctx.food_servo_index, i)
        sleep(0.02)

    for i in range(1500, 500, -20):
        Ctx.pwm.setServoPulse(Ctx.food_servo_index, i)
        sleep(0.02)
    # put water
    # GPIO.output(Ctx.water_in_index, GPIO.HIGH)
    # sleep(0.5)
    # GPIO.output(Ctx.water_in_index, GPIO.LOW)

    Ctx.STATUS = "FoodPrepared"


def stream():
    # put water
    for _ in range(1):
        GPIO.output(Ctx.water_out_index, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(Ctx.water_out_index, GPIO.LOW)


def clean():
    for _ in range(2):
        # put water
        GPIO.output(Ctx.water_in_index, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(Ctx.water_in_index, GPIO.LOW)

        # thrash water
        GPIO.output(Ctx.water_out_index, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(Ctx.water_out_index, GPIO.LOW)

    Ctx.STATUS = "Cleaned"


def finalize():
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
