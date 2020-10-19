from time import sleep

from python.zaf2.context import Context
from python.zaf2.control_box import ControlBox


def demo_valves(valves):
    cbox = ControlBox()

    # Make sure all valves closed before start
    i = 0
    while i < 31:
        cbox.close_valve(i)
        print(i)
        i += 1

    # Open the valves requested
    for valve in valves:
        cbox.open_valve(valve)
        print(valve)
        sleep(1)

    # Close them back
    for valve in valves:
        cbox.close_valve(valve)
        print(valve)
        sleep(1)

    cbox.close_valve(4)

    # Make sure all valves closed after finish
    i = 0
    while i < 31:
        cbox.close_valve(i)
        print(i)
        i += 1


def demo_pumps(pumps, duration=0.5):
    ctx = Context()
    Context.initialize()
    ctx.run_pump(pumps, duration=duration)


if __name__ == '__main__':
    # Use the following line with list of indices to test pumps
    demo_pumps(pumps=[0, 3, 5], duration=0.5)

    # Use the following line with list of indices to test pumps
    # demo_valves(valves=[0, 3, 5])


