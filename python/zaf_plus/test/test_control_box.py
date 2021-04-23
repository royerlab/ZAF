from time import sleep

from python.zaf_plus.control_box import ControlBox


def test_initialize():
    ctrl_box = ControlBox()

    for _ in range(10):
        ctrl_box.initialize()
        sleep(1)

    for _ in range(10):
        ctrl_box.initialize()
        sleep(0.1)


def test_open_and_close_valve():
    ctrl_box = ControlBox()
    ctrl_box.initialize()

    for _ in range(10):
        ctrl_box.open_valve(_)
        sleep(0.1)
        ctrl_box.close_valve(_)


def test_set_pwm():
    ctrl_box = ControlBox()
    ctrl_box.initialize()

    ctrl_box.initialize()

    for _ in range(10):
        ctrl_box.set_pwm(5, 180)
        sleep(0.1)
        ctrl_box.set_pwm(5, 0)


if __name__ == '__main__':
    # test_initialize()
    # test_open_and_close_valve()
    test_set_pwm()
