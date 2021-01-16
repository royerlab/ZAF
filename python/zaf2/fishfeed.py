import datetime
from time import sleep
from RPi import GPIO
from arbol.arbol import lprint, section

from python.gui.widgets.worker import Worker
from python.zaf2.context import Context


@section('initialize function')
def initialize():
    Context.initialize()

    if not Context.early_stop:
        Context.DAY, Context.TIME = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S').split()
        # Initialize water sensor
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Context.water_sensor, GPIO.OUT)
        GPIO.output(Context.water_sensor, GPIO.LOW)
        sleep(0.05)
        GPIO.setup(Context.water_sensor, GPIO.IN)

        lprint("initialized")


@section('priming function')
def priming(valves_in_use):
    # Open all valves
    for valve in valves_in_use:
        Context.control_box.open_valve(valve)
        # prime water In
        for _ in range(1):
            Context.check_water_sensor()
            Context.run_pump(Context.water_in, duration=10)
        # prime water Out
        for _ in range(1):
            Context.check_water_sensor()
            Context.run_pump(Context.water_out1, duration=8)
        Context.control_box.close_valve(valve)

    # # Close all valves
    # for valve in valves_in_use:
    #     Context.control_box.close_valve(valve)

    lprint("pumps primed")


@section('prepare function')
def prepare():
    # pour food into fishfeeder
    Context.rotate_food_servo(180)
    Context.rotate_food_servo(0)

    Context.rotate_food_servo(180)
    Context.rotate_food_servo(0)

    # bring clean water to fishfeeder
    for _ in range(1):
        Context.check_water_sensor()
        Context.run_pump(Context.water_in, duration=2)
    Context.STATUS = "FoodPrepared"

    lprint("food prepared")


@section('stream function')
def stream():
    # stream water to fish tanks
    for i in range(3):
        Context.check_water_sensor()
        Context.run_pump(Context.water_out1, duration=0.5)
    # bring water and stream fishfeeder
    for _ in range(2):
        for _ in range(1):
            Context.check_water_sensor()
            Context.run_pump(Context.water_in, duration=1)
        for _ in range(2):
            Context.check_water_sensor()
            Context.run_pump(Context.water_out1, duration=1)

    lprint("food water mix streamed")


@section('clean function')
def clean():
    for _ in range(1):
        # bring clean water to fishfeeder
        Context.check_water_sensor()
        Context.run_pump(Context.water_in, duration=0.5)
    for _ in range(3):
        # thrash water from fishfeeder
        Context.check_water_sensor()
        Context.run_pump(Context.water_out1, duration=2)
    for _ in range(2):
        for _ in range(1):
            # bring clean water to fishfeeder
            Context.check_water_sensor()
            Context.run_pump(Context.water_in, duration=0.5)
        for _ in range(2):
            # thrash water from fishfeeder
            Context.check_water_sensor()
            Context.run_pump(Context.water_out1, duration=0.5)
    for _ in range(1):
                # bring clean water to fishfeeder
                Context.check_water_sensor()
                Context.run_pump(Context.water_in, duration=3)
    for _ in range(1):
                # thrash water from fishfeeder
                Context.check_water_sensor()
                Context.run_pump(Context.water_out1, duration=10)
    Context.STATUS = "Cleaned"

    lprint("tanks cleaned")


@section('finalize function')
def finalize():
    if not Context.early_stop:
        Context.control_box.set_pwm(Context.safety_pump, 0)
        lprint(Context.DAY, Context.TIME, Context.STATUS)

        lprint("finalized")


def run(progress_callback, check_early_stop):
    valves_in_use_feeding = [27]

    try:
        # initialize ports
        if not check_early_stop():
            initialize()

        # # Run feeding sequence for each tank
        # for valve in valves_in_use_feeding:
        #     # priming pumps
        #     priming([valve])
        #
        #     # prepare food
        #     prepare()
        #
        #     # open the current right valve
        #     Context.control_box.open_valve(valve)
        #
        #     # deliver food to containers
        #     stream()
        #
        #     # clean the tank
        #     clean()
        #
        #     # close the opened valve
        #     Context.control_box.close_valve(valve)

    except KeyboardInterrupt:
        print("\nCtrl-C pressed.  Program exiting...")
    finally:
        # finalize
        if not check_early_stop():
            finalize()


if __name__ == '__main__':
    run()
