
import _io
from serial import *

uart = Serial()

"""
def serial_port_send_file(UART: Serial, file: _io):
    num_bytes = file.__sizeof__()
    UART.write(file, num_bytes)
    
    pass

"""


def serial_port_send_command(UART: Serial, data: str):
    """
    this function is used to transmit commands through serial port,
    it includes mechanism which encodes data as ASCII (bytes, b encoding)
    """
    if UART.isOpen():
        data_to_send = data.encode(encoding="ascii", errors="replace")
        UART.write(data_to_send)

    else:   # in the future, here, it would be possible to add statement raise exception
        pass


def serial_port_read_bytes():
    pass


def serial_port_read_to_file(UART: Serial, file: _io.FileIO, num_bytes: int):

    if UART.isOpen():

        file.write(str(UART.read(num_bytes)))

    else:   # in the future, here, it would be possible to add statement raise exception
        pass
