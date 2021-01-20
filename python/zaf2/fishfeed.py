import datetime
from time import sleep
from RPi import GPIO
from arbol.arbol import lprint, section

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


@section('general water priming function')
def general_priming(valves_in_use_feeding):
    for valve in valves_in_use_feeding:
        Context.control_box.open_valve(valve)
        Context.run_pump(Context.water_in, duration=0.5)
        Context.run_pump(Context.water_out1, duration=4)
        Context.control_box.close_valve(valve)

    lprint("General_priming_done")

@section('general water priming function')
def general_priming(valves_in_use_feeding):
    for valve in valves_in_use_feeding:
        Context.control_box.open_valve(valve)
        Context.run_pump(Context.water_in, duration=0.5)
        Context.run_pump(Context.water_out1, duration=4)
        Context.control_box.close_valve(valve)

    lprint("General_priming_done")


@section('priming function')
def priming(valves_in_use_feeding):
    # Open all valves
    for valve in valves_in_use_feeding:
        Context.control_box.open_valve(valve)
        # prime water In
        for _ in range(1):
            Context.check_water_sensor()
            Context.run_pump(Context.water_in, duration=0.5)
        # prime water Out
        for _ in range(1):
            Context.check_water_sensor()
            Context.run_pump(Context.water_out1, duration=3)
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


    # bring clean water to fishfeeder
    #for _ in range(1):
        #Context.check_water_sensor()
        #Context.run_pump(Context.water_in, duration=0.5)
    #Context.STATUS = "FoodPrepared"

    lprint("food prepared")


@section('stream function')
def stream():
    # stream water to fish tanks
    for i in range(2):
        Context.check_water_sensor()
        Context.run_pump(Context.water_out1, duration=1)
    # bring water and stream fishfeeder
    for _ in range(1):
        Context.check_water_sensor()
        Context.control_box.set_pwm(Context.water_in, 255)
        Context.control_box.set_pwm(Context.water_out1, 255)
        sleep(0.5)
        Context.control_box.set_pwm(Context.water_in, 0)
        Context.control_box.set_pwm(Context.water_out1, 0)
        Context.run_pump(Context.water_out1, duration=1)

        #for _ in range(1):
            #Context.check_water_sensor()
            #Context.run_pump(Context.water_in, duration=1)
        #for _ in range(1):
            #Context.check_water_sensor()
            #Context.run_pump(Context.water_out1, duration=2)

    lprint("food water mix streamed")


@section('clean function')
def clean():
    for _ in range(1):
        # bring clean water to fishfeeder
        Context.check_water_sensor()
        Context.run_pump(Context.water_in, duration=0.25)
        # thrash water from fishfeeder
        Context.check_water_sensor()
        Context.run_pump(Context.water_out1, duration=2)
    for _ in range(1):
        for _ in range(1):
            # bring clean water to fishfeeder
            Context.check_water_sensor()
            Context.run_pump(Context.water_in, duration=0.25)
        for _ in range(1):
            # thrash water from fishfeeder
            Context.check_water_sensor()
            Context.run_pump(Context.water_out1, duration=1)
    for _ in range(1):
                # bring clean water to fishfeeder
                Context.check_water_sensor()
                Context.run_pump(Context.water_in, duration=2)
    for _ in range(1):
                # thrash water from fishfeeder
                Context.check_water_sensor()
                Context.run_pump(Context.water_out1, duration=20)
    Context.STATUS = "Cleaned"

    lprint("tanks cleaned")


@section('general air cleaning')
def air_cleaning(valves_in_use_feeding):
    for valve in valves_in_use_feeding:
        Context.control_box.open_valve(valve)
        Context.run_pump(Context.water_out1, duration=10)
        Context.control_box.close_valve(valve)

    lprint("Air_cleaning_done")


@section('finalize function')
def finalize():
    if not Context.early_stop:
        Context.control_box.set_pwm(Context.safety_pump, 0)
        lprint(Context.DAY, Context.TIME, Context.STATUS)

        lprint("finalized")


def run(progress_callback, check_early_stop):
    valves_in_use_feeding = [24]

    try:
        # initialize ports
        if not check_early_stop():
            initialize()

        # clean all the tube with water
        general_priming(valves_in_use_feeding)

        # clean all the tube with water
        general_priming(valves_in_use_feeding)

        # Run feeding sequence for each tank
        for valve in valves_in_use_feeding:
            # priming pumps
            priming([valve])

            # prepare food
            prepare()

            # open the current right valve
            Context.control_box.open_valve(valve)

            # deliver food to containers
            stream()

            # clean the tank
            clean()

            # close the opened valve
            Context.control_box.close_valve(valve)

        # clean all the tube with air
        air_cleaning(valves_in_use_feeding)

    except KeyboardInterrupt:
        print("\nCtrl-C pressed.  Program exiting...")
    finally:
        # finalize
        if not check_early_stop():
            finalize()


if __name__ == '__main__':
    run()
