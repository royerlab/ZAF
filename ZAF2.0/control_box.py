from time import sleep

import serial


class ControlBox:

    def __init__(self, port="/dev/ttyACM0", rate=500000,  nb_arduino=2):
        self.port = port
        self.rate = rate
        self.nb_arduino = nb_arduino

        self.conn = serial.Serial(self.port, baudrate=self.rate, timeout=2.0)
        self.conn.flushInput()

    get_state = str.encode("#?\n")
    shutdown_all = str.encode("#!\n")
    debug = lambda x: str.encode("#d" + str(int(x)) + "\n'")

    test_valves = str.encode("#tv 3\n")

    def initialize(self):
        self.conn.write(self.get_state)
        rcv = self.conn.read(43)
        print(rcv)

        self.conn.write(self.get_state)
        rcv = self.conn.read(78)
        print(rcv)
        rcv = self.conn.read(78)
        print(rcv)

    def open_valve(self, index):
        open_valve_command = str.encode(f"#vo {index} \n")

        self.conn.write(open_valve_command)
        rcv = self.conn.read(6)
        print(rcv)
        sleep(1)

    def close_valve(self, index):
        close_valve_command = str.encode(f"#vc {index} \n")

        self.conn.write(close_valve_command)
        rcv = self.conn.read(6)
        print(rcv)
        sleep(1)

    def set_pwm(self, index, value):
        set_pwm_command = str.encode(f"#p {index} {value} \n")

        self.conn.write(set_pwm_command)
        rcv = self.conn.read(6)
        print(rcv)
        sleep(1)
