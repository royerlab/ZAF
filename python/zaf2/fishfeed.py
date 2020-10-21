import datetime
from time import sleep
from RPi import GPIO

from context import Context


def initialize():
    Context.initialize()

    Context.DAY, Context.TIME = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S').split()

    # Initialize water sensor
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(Context.water_sensor, GPIO.OUT)
    GPIO.output(Context.water_sensor, GPIO.LOW)
    sleep(0.05)
    GPIO.setup(Context.water_sensor, GPIO.IN)


def priming(valves_in_use):
    # Open all valves
    for valve in valves_in_use:
        Context.control_box.open_valve(valve)

    # prime water In
    for _ in range(3):
        Context.check_water_sensor()
        Context.run_pump([Context.water_in], duration=0.5)

    # prime water Out
    for _ in range(1):
        Context.check_water_sensor()
        Context.run_pump(pumps=[Context.water_out1, Context.water_out2], duration=0.5)

    # Close all valves
    for valve in valves_in_use:
        Context.control_box.close_valve(valve)


def prepare():
    # pour food into fishfeeder
    Context.rotate_food_servo(180)
    Context.rotate_food_servo(0)

    # bring clean water to fishfeeder
    for _ in range(1):
        Context.check_water_sensor()
        Context.run_pump(pumps=[Context.water_in], duration=0.5)

    Context.STATUS = "FoodPrepared"


def stream():
    # stream water to fish tanks
    for i in range(1):
        for _ in range(1):
            Context.check_water_sensor()
            Context.run_pump(pumps=[Context.water_out1, Context.water_out2], duration=0.5)

    # bring water and stream fishfeeder
    for _ in range(1):
        for _ in range(1):
            Context.check_water_sensor()
            Context.run_pump(pumps=[Context.water_in], duration=0.5)

        for _ in range(1):
            Context.check_water_sensor()
            Context.run_pump(pumps=[Context.water_out1, Context.water_out2], duration=0.5)


def clean():
    for _ in range(1):
        # bring clean water to fishfeeder
        Context.check_water_sensor()
        Context.run_pump(pumps=[Context.water_in], duration=0.5)

    for _ in range(1):
        # thrash water from fishfeeder
        Context.check_water_sensor()
        Context.run_pump(pumps=[Context.water_out1, Context.water_out2], duration=0.5)

    for _ in range(1):
        for _ in range(1):
            # bring clean water to fishfeeder
            Context.check_water_sensor()
            Context.run_pump(pumps=[Context.water_in], duration=0.5)

        for _ in range(1):
            # thrash water from fishfeeder
            Context.check_water_sensor()
            Context.run_pump(pumps=[Context.water_out1, Context.water_out2], duration=0.5)

    for _ in range(1):
        for _ in range(1):
            # bring clean water to fishfeeder
            Context.check_water_sensor()
            Context.run_pump(pumps=[Context.water_in], duration=0.5)

        for _ in range(1):
            # thrash water from fishfeeder
            Context.check_water_sensor()
            Context.run_pump(pumps=[Context.water_out1, Context.water_out2], duration=0.5)

    Context.STATUS = "Cleaned"


def finalize():
    Context.control_box.set_pwm(Context.safety_pump, 0)
    print(Context.DAY, Context.TIME, Context.STATUS)


def run():
    valves_in_use = range(1)

    try:
        # initialize ports
        initialize()
        print("initialized")

        # Run feeding sequence for each tank
        for valve in valves_in_use:
            # priming pumps
            priming(valves_in_use)
            print("pumps primed")

            # prepare food
            prepare()
            print("food prepared")

            # open the current right valve
            Context.control_box.open_valve(valve)

            # deliver food to containers
            stream()
            print("food water mix streamed")

            # clean the tank
            clean()
            print("tanks cleaned")

            # close the opened valve
            Context.control_box.close_valve(valve)

    except KeyboardInterrupt:
        print("\nCtrl-C pressed.  Program exiting...")
    finally:
        # finalize
        finalize()
        print("finalized")


if __name__ == '__main__':
    run()
