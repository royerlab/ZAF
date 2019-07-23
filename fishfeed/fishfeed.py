import datetime
from time import sleep



def initialize():
    Ctx.DAY, Ctx.TIME = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S').split()
    Ctx.pwm.setPWMFreq(50)

def prepare():
    # put food

    # put water

def stream():
    pass

def clean():
    for _ in range(2):
        # put water

        # thrash water


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
