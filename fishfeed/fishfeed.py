import datetime
from time import sleep

from RPi import GPIO

from ctx import Ctx


def initialize():
    # Set day and time to keep log
    Ctx.DAY, Ctx.TIME = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S').split()

    # Set pin layout indices to BCM mode
    GPIO.setmode(GPIO.BCM)

    # Initialize water sensor
    GPIO.setup(Ctx.water_sensor, GPIO.OUT)
    GPIO.output(Ctx.water_sensor, GPIO.LOW)
    sleep(0.05)
    GPIO.setup(Ctx.water_sensor, GPIO.IN)

    # Initialize food servo
    GPIO.setup(Ctx.food_servo_index, GPIO.OUT)
    Ctx.pwm = GPIO.PWM(Ctx.food_servo_index, 50)  # GPIO 17 for PWM with 50Hz
    Ctx.pwm.start(2.5)  # Initialization of the food servo

    # Initialize all pumps
    GPIO.setup(Ctx.water_in_high, GPIO.OUT)
    GPIO.output(Ctx.water_in_high, GPIO.LOW)

    GPIO.setup(Ctx.water_in_low, GPIO.OUT)
    GPIO.output(Ctx.water_in_low, GPIO.LOW)

    GPIO.setup(Ctx.safety_pump_high, GPIO.OUT)
    GPIO.output(Ctx.water_in_high, GPIO.LOW)

    GPIO.setup(Ctx.safety_pump_low, GPIO.OUT)
    GPIO.output(Ctx.safety_pump_low, GPIO.LOW)

    GPIO.setup(Ctx.water_out1_high, GPIO.OUT)
    GPIO.output(Ctx.water_out1_high, GPIO.LOW)

    GPIO.setup(Ctx.water_out1_low, GPIO.OUT)
    GPIO.output(Ctx.water_out1_low, GPIO.LOW)

    GPIO.setup(Ctx.water_out2_high, GPIO.OUT)
    GPIO.output(Ctx.water_out2_high, GPIO.LOW)

    GPIO.setup(Ctx.water_out2_low, GPIO.OUT)
    GPIO.output(Ctx.water_out2_low, GPIO.LOW)

    GPIO.setup(Ctx.air_pump_high, GPIO.OUT)
    GPIO.output(Ctx.air_pump_high, GPIO.LOW)

    GPIO.setup(Ctx.air_pump_low, GPIO.OUT)
    GPIO.output(Ctx.air_pump_low, GPIO.LOW)

    # air and safety on
    GPIO.output(Ctx.air_pump_high, GPIO.HIGH)
    GPIO.output(Ctx.air_pump_low, GPIO.LOW)


def prepare():
    # pour food into fishfeeder
    for i in range(0, 25, 1):
        Ctx.pwm.ChangeDutyCycle(i)
        sleep(0.02)

    for i in range(25, 0, -1):
        Ctx.pwm.ChangeDutyCycle(i)
        sleep(0.02)

    # bring clean water to fishfeeder
    for _ in range(20):
        check_water_sensor()
        GPIO.output(Ctx.water_in_high, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(Ctx.water_in_high, GPIO.LOW)

    Ctx.STATUS = "FoodPrepared"


def stream():
    # stream water to fish tanks
    for i in range(1):
        for _ in range(30):
            check_water_sensor()
            GPIO.output(Ctx.water_out1_high, GPIO.HIGH)
            GPIO.output(Ctx.water_out2_high, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(Ctx.water_out1_high, GPIO.LOW)
            GPIO.output(Ctx.water_out2_high, GPIO.LOW)


    # bring water and stream fishfeeder
    for _ in range(5):
            for _ in range(3):
                check_water_sensor()
                GPIO.output(Ctx.water_in_high, GPIO.HIGH)
                sleep(0.5)
                GPIO.output(Ctx.water_in_high, GPIO.LOW)

            for _ in range(5):
                check_water_sensor()
                GPIO.output(Ctx.water_out1_high, GPIO.HIGH)
                GPIO.output(Ctx.water_out2_high, GPIO.HIGH)
                sleep(0.5)
                GPIO.output(Ctx.water_out1_high, GPIO.LOW)
                GPIO.output(Ctx.water_out2_high, GPIO.LOW)


def clean():
    for _ in range(3):
        for _ in range(20):
        # bring clean water to fishfeeder
            check_water_sensor()
            GPIO.output(Ctx.water_in_high, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(Ctx.water_in_high, GPIO.LOW)

        for _ in range(25):
        # thrash water from fishfeeder
            check_water_sensor()
            GPIO.output(Ctx.water_out1_high, GPIO.HIGH)
            GPIO.output(Ctx.water_out2_high, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(Ctx.water_out1_high, GPIO.LOW)
            GPIO.output(Ctx.water_out2_high, GPIO.LOW)

    Ctx.STATUS = "Cleaned"


def finalize():
    GPIO.output(Ctx.water_in_high, GPIO.LOW)
    GPIO.output(Ctx.water_out1_high, GPIO.LOW)
    GPIO.output(Ctx.water_out2_high, GPIO.LOW)
    GPIO.output(Ctx.air_pump_high, GPIO.LOW)
    GPIO.output(Ctx.safety_pump_high, GPIO.LOW)

    print Ctx.DAY, Ctx.TIME, Ctx.STATUS


def check_water_sensor():
    if GPIO.input(Ctx.water_sensor) == GPIO.LOW:
        print("no water warning by sensor")
        GPIO.output(Ctx.safety_pump_high, GPIO.LOW)
    else:
        GPIO.output(Ctx.safety_pump_high, GPIO.HIGH)
        print("WATER WARNING by sensor")


def run():

    try:
        # initialize ports
        initialize()
        print("initialized")

        # prepare food
        prepare()
        print("food prepared")
        #
        # # deliver food to containers
        # stream()
        # print("food water mix streamed")
        #
        # # clean the tank
        # clean()
        # print("tanks cleaned")

    except KeyboardInterrupt:
        print("\nCtrl-C pressed.  Program exiting...")
    finally:
        # finalize
        finalize()
        print("finalized")

        GPIO.cleanup()  # run on exit


if __name__ == '__main__':
    run()
