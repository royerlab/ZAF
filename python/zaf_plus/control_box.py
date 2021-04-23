from time import sleep
import serial
from arbol.arbol import lprint


class ControlBox:

    def __init__(self, port="/dev/ttyACM0", rate=500000,  nb_arduino=2):
        self.port = port
        self.rate = rate
        self.nb_arduino = nb_arduino

        self.first_time = True

        try:
            self.conn = serial.Serial(self.port, baudrate=self.rate, timeout=2.0)
        except:
            try:
                self.port = "/dev/ttyACM1"
                self.conn = serial.Serial(self.port, baudrate=self.rate, timeout=2.0)
            except:
                try:
                    self.port = "/dev/ttyACM2"
                    self.conn = serial.Serial(self.port, baudrate=self.rate, timeout=2.0)
                except:
                    raise ConnectionError("Couldn't connect to ControlBox")

        self.conn.flushInput()

    get_state = str.encode("#?\n")
    shutdown_all = str.encode("#!\n")
    debug = lambda x: str.encode("#d" + str(int(x)) + "\n'")

    test_valves = str.encode("#tv 3\n")

    def initialize(self):
        if self.first_time:
            self.conn.write(self.get_state)
            rcv = self.conn.read(43)
            lprint(rcv)
            self.first_time = False

        self.conn.write(self.get_state)
        rcv = self.conn.read(78)
        lprint(rcv)
        rcv = self.conn.read(78)
        lprint(rcv)

    def open_valve(self, index):
        open_valve_command = str.encode(f"#vo {index} \n")

        self.conn.write(open_valve_command)
        rcv = self.conn.read(6)
        lprint(f"opened valve index:{index}, rcv:{rcv}")
        sleep(1)

    def close_valve(self, index):
        close_valve_command = str.encode(f"#vc {index} \n")

        self.conn.write(close_valve_command)
        rcv = self.conn.read(6)
        lprint(f"closed valve index:{index}, rcv:{rcv}")
        sleep(1)

    def set_pwm(self, index, value):
        set_pwm_command = str.encode(f"#p {index} {value} \n")

        self.conn.write(set_pwm_command)
        rcv = self.conn.read(6)
        lprint(f"set_pwm index:{index}, value:{value}, rcv:{rcv}")
        sleep(1)
