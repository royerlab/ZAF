import datetime
import json
import sys
from time import sleep
from RPi import GPIO
from arbol.arbol import lprint, section

from python.zaf2.context import Context
# from context import Context


class FishFeed:
    def __init__(self,
                 progress_callback,
                 check_early_stop,
                 valves_in_use_feeding=None
    ):
        self.progress_callback = progress_callback
        self.check_early_stop = check_early_stop
        self.valves_in_use_feeding = valves_in_use_feeding

    @section('initialize function')
    def initialize(self):
        Context.initialize()

        if not self.check_early_stop():
            Context.DAY, Context.TIME = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S').split()
            # Initialize water sensor
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(Context.water_sensor, GPIO.OUT)
            GPIO.output(Context.water_sensor, GPIO.LOW)
            sleep(0.05)
            GPIO.setup(Context.water_sensor, GPIO.IN)

            lprint("initialized")

    @section('general water priming function')
    def general_priming(self):
        for valve in self.valves_in_use_feeding:
            Context.control_box.open_valve(valve)
            Context.run_pump(Context.water_in, duration=0.5)
            Context.run_pump(Context.water_out1, duration=4)
            Context.control_box.close_valve(valve)

        lprint("General_priming_done")

    @section('priming function')
    def priming(self, valves_in_use_feeding):
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
    def prepare(self, food_amount_multiplier):
        # pour food into fishfeeder
        for _ in range(food_amount_multiplier):
            Context.rotate_food_servo(180)
            Context.rotate_food_servo(0)


        # bring clean water to fishfeeder
        #for _ in range(1):
            #Context.check_water_sensor()
            #Context.run_pump(Context.water_in, duration=0.5)
        #Context.STATUS = "FoodPrepared"

        lprint("food prepared")

    @section('stream function')
    def stream(self):
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
    def clean(self):
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
    def air_cleaning(self):
        for valve in self.valves_in_use_feeding:
            Context.control_box.open_valve(valve)
            Context.run_pump(Context.water_out1, duration=10)
            Context.control_box.close_valve(valve)

        lprint("Air_cleaning_done")

    @section('finalize function')
    def finalize(self):
        if not self.check_early_stop():
            Context.control_box.set_pwm(Context.safety_pump, 0)
            lprint(Context.DAY, Context.TIME, Context.STATUS)

            lprint("finalized")


def run(progress_callback, check_early_stop, food_amounts=None):

    valves_in_use_feeding = [i for i in range(len(food_amounts)) if food_amounts[i] is not None]

    feeder = FishFeed(progress_callback, check_early_stop, valves_in_use_feeding=valves_in_use_feeding)

    try:
        # initialize ports
        if not feeder.check_early_stop():
            feeder.initialize()

        # clean all the tube with water
        feeder.general_priming()

        # clean all the tube with water
        feeder.general_priming()

        # Run feeding sequence for each tank
        for valve in valves_in_use_feeding:
            # priming pumps
            feeder.priming([valve])

            # prepare food
            feeder.prepare(int(food_amounts[valve]))

            # open the current right valve
            Context.control_box.open_valve(valve)

            # deliver food to containers
            feeder.stream()

            # clean the tank
            feeder.clean()

            # close the opened valve
            Context.control_box.close_valve(valve)

        # clean all the tube with air
        feeder.air_cleaning()

    except KeyboardInterrupt:
        print("\nCtrl-C pressed.  Program exiting...")
    finally:
        # finalize
        if not feeder.check_early_stop():
            feeder.finalize()


def fake_check_early_stop():
    return False


if __name__ == '__main__':

    json_path = sys.argv[1]

    with open(json_path, "r") as read_file:
        data = json.load(read_file)

        run(None, fake_check_early_stop, food_amounts=data["Tanks"])

    # run(None, fake_check_early_stop, food_amounts=[4])
