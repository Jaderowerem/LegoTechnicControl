import _io
# import os
from serial import *

uart = Serial()

"""
def serial_port_send_file(UART: Serial, file: _io.TextIOWrapper):
    num_bytes = file.__sizeof__()
    UART.write(file, num_bytes)
    
    pass

"""


def serial_port_send_command(UART: Serial, data: str):

    data_to_send = data.encode(encoding="ascii", errors="replace")
    UART.write(data_to_send)


def serial_port_read_bytes():
    pass


def serial_port_read_to_file():
    pass
