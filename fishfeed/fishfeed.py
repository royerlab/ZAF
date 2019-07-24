import datetime
from time import sleep

from fishfeed.ctx import Ctx


def initialize():
    Ctx.DAY, Ctx.TIME = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S').split()
    Ctx.pwm.setPWMFreq(50)

def prepare():
    # put food
    for i in range(500, 1500, 20):
        Ctx.pwm.setServoPulse(Ctx.food_servo_index, i)
        sleep(0.02)

    for i in range(1500, 500, -20):
        Ctx.pwm.setServoPulse(Ctx.food_servo_index, i)
        sleep(0.02)
    # put water
    Ctx.pwm.setPWM(Ctx.water_in_index, 0, 2048)
    sleep(2.5)
    Ctx.pwm.setPWM(Ctx.water_in_index, 0, 0)


def stream():
    # put water
    Ctx.pwm.setPWM(Ctx.green_pump_index, 0, 2048)
    Ctx.pwm.setPWM(Ctx.pink_pump_index, 0, 2048)
    Ctx.pwm.setPWM(Ctx.red_pump_index, 0, 2048)
    sleep(2.5)
    Ctx.pwm.setPWM(Ctx.green_pump_index, 0, 0)
    Ctx.pwm.setPWM(Ctx.pink_pump_index, 0, 0)
    Ctx.pwm.setPWM(Ctx.red_pump_index, 0, 0)


def clean():
    for _ in range(2):
        # put water
        Ctx.pwm.setPWM(Ctx.water_in_index, 0, 2048)
        sleep(0.5)
        Ctx.pwm.setPWM(Ctx.water_in_index, 0, 0)

        # thrash water
        Ctx.pwm.setPWM(Ctx.water_out_index, 0, 2048)
        sleep(0.5)
        Ctx.pwm.setPWM(Ctx.water_out_index, 0, 0)

    Ctx.STATUS = "Cleaned"


def finalize():
    print Ctx.DAY, Ctx.TIME, Ctx.STATUS


def run():
    # initialize ports
    initialize()

    # prepare food
    prepare()

    # stream
    stream()

    # clean
    clean()

    # finalize
    finalize()
