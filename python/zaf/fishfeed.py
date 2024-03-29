import datetime
from time import sleep
from RPi import GPIO

from python.zaf.PCA9685 import PCA9685
from python.zaf.ctx import Ctx


def initialize():
    Ctx.DAY, Ctx.TIME = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S').split()

    # Set pin layout indices to BCM mode
    GPIO.setmode(GPIO.BCM)

    # Initialize water sensor
    GPIO.setup(Ctx.water_sensor, GPIO.OUT)
    GPIO.output(Ctx.water_sensor, GPIO.LOW)
    sleep(0.05)
    GPIO.setup(Ctx.water_sensor, GPIO.IN)

    # Initialize
    Ctx.pwm = PCA9685(0x40, debug=False)
    Ctx.pwm.setPWMFreq(50)

    # air and safety on
    Ctx.pwm.setPWM(Ctx.air_pump, 0, 4095)

    # solenoid open
    Ctx.pwm.setPWM(Ctx.water_in_solenoid, 0, 4095)

def priming ():
    # prime wateter In
    for _ in range(15):
        check_water_sensor()
        Ctx.pwm.setPWM(Ctx.water_in, 0, 4095)
        sleep(0.5)
        Ctx.pwm.setPWM(Ctx.water_in, 0, 0)

    # prime water Out
    for _ in range(5):
        check_water_sensor()
        Ctx.pwm.setPWM(Ctx.water_out1, 0, 4095)
        Ctx.pwm.setPWM(Ctx.water_out2, 0, 4095)
        sleep(0.5)
        Ctx.pwm.setPWM(Ctx.water_out1, 0, 0)
        Ctx.pwm.setPWM(Ctx.water_out2, 0, 0)


def prepare():
    # pour food into fishfeeder
    for i in range(500, 1700, 30):
        Ctx.pwm.setServoPulse(0, i)
        sleep(0.02)

    for i in range(1700, 500, -30):
        Ctx.pwm.setServoPulse(0, i)
        sleep(0.02)

    # bring clean water to fishfeeder
    for _ in range(10):
        check_water_sensor()
        Ctx.pwm.setPWM(Ctx.water_in, 0, 4095)
        sleep(0.5)
        Ctx.pwm.setPWM(Ctx.water_in, 0, 0)

    Ctx.STATUS = "FoodPrepared"


def stream():
    # stream water to fish tanks
    for i in range(1):
        for _ in range(6):
            check_water_sensor()
            Ctx.pwm.setPWM(Ctx.water_out1, 0, 4095)
            Ctx.pwm.setPWM(Ctx.water_out2, 0, 4095)
            sleep(0.5)
            Ctx.pwm.setPWM(Ctx.water_out1, 0, 0)
            Ctx.pwm.setPWM(Ctx.water_out2, 0, 0)

    # bring water and stream fishfeeder
    for _ in range(2):
            for _ in range(8):
                check_water_sensor()
                Ctx.pwm.setPWM(Ctx.water_in, 0, 4095)
                sleep(0.5)
                Ctx.pwm.setPWM(Ctx.water_in, 0, 0)

            for _ in range(6):
                check_water_sensor()
                Ctx.pwm.setPWM(Ctx.water_out1, 0, 4095)
                Ctx.pwm.setPWM(Ctx.water_out2, 0, 4095)
                sleep(0.5)
                Ctx.pwm.setPWM(Ctx.water_out1, 0, 0)
                Ctx.pwm.setPWM(Ctx.water_out2, 0, 0)


def clean():
    for _ in range(9):
        # bring clean water to fishfeeder
        check_water_sensor()
        Ctx.pwm.setPWM(Ctx.water_in, 0, 4095)
        sleep(0.5)
        Ctx.pwm.setPWM(Ctx.water_in, 0, 0)

    for _ in range(5):
        # thrash water from fishfeeder
        check_water_sensor()
        Ctx.pwm.setPWM(Ctx.water_out1, 0, 4095)
        Ctx.pwm.setPWM(Ctx.water_out2, 0, 4095)
        sleep(0.5)
        Ctx.pwm.setPWM(Ctx.water_out1, 0, 0)
        Ctx.pwm.setPWM(Ctx.water_out2, 0, 0)

    for _ in range(3):
        for _ in range(9):
        # bring clean water to fishfeeder
            check_water_sensor()
            Ctx.pwm.setPWM(Ctx.water_in, 0, 4095)
            sleep(0.5)
            Ctx.pwm.setPWM(Ctx.water_in, 0, 0)

        for _ in range(5):
        # thrash water from fishfeeder
            check_water_sensor()
            Ctx.pwm.setPWM(Ctx.water_out1, 0, 4095)
            Ctx.pwm.setPWM(Ctx.water_out2, 0, 4095)
            sleep(0.5)
            Ctx.pwm.setPWM(Ctx.water_out1, 0, 0)
            Ctx.pwm.setPWM(Ctx.water_out2, 0, 0)

    for _ in range(3):
         for _ in range(10):
                # bring clean water to fishfeeder
                check_water_sensor()
                Ctx.pwm.setPWM(Ctx.water_in, 0, 4095)
                sleep(0.5)
                Ctx.pwm.setPWM(Ctx.water_in, 0, 0)

         for _ in range(6):
                # thrash water from fishfeeder
                check_water_sensor()
                Ctx.pwm.setPWM(Ctx.water_out1, 0, 4095)
                Ctx.pwm.setPWM(Ctx.water_out2, 0, 4095)
                sleep(0.5)
                Ctx.pwm.setPWM(Ctx.water_out1, 0, 0)
                Ctx.pwm.setPWM(Ctx.water_out2, 0, 0)

    Ctx.STATUS = "Cleaned"


def finalize():
    Ctx.pwm.setPWM(Ctx.water_in, 0, 0)
    Ctx.pwm.setPWM(Ctx.water_out1, 0, 0)
    Ctx.pwm.setPWM(Ctx.water_out2, 0, 0)
    Ctx.pwm.setPWM(Ctx.air_pump, 0, 0)
    Ctx.pwm.setPWM(Ctx.safety_pump, 0, 0)
    # solenoid close
    Ctx.pwm.setPWM(Ctx.water_in_solenoid, 0, 0)

    print Ctx.DAY, Ctx.TIME, Ctx.STATUS


def check_water_sensor():
    if GPIO.input(Ctx.water_sensor) == GPIO.LOW:
        print("no water warning by sensor")
        Ctx.pwm.setPWM(Ctx.safety_pump, 0, 0)
    else:
        Ctx.pwm.setPWM(Ctx.safety_pump, 0, 4095)
        print("WATER WARNING by sensor")


def run_fishfeed():

    try:
        # initialize ports
        initialize()
        print("initialized")

        # priming pumps
        priming()
        print("pumps primed")

        # prepare food
        prepare()
        print("food prepared")

        # deliver food to containers
        stream()
        print("food water mix streamed")

        # clean the tank
        clean()
        print("tanks cleaned")

    except KeyboardInterrupt:
        print("\nCtrl-C pressed.  Program exiting...")
    finally:
        # finalize
        finalize()
        print("finalized")

        GPIO.cleanup()  # run on exit


if __name__ == '__main__':
    run_fishfeed()
