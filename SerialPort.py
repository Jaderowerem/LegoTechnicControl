import PySimpleGUI
from serial import *
from typing import BinaryIO

uart = Serial(bytesize=EIGHTBITS, timeout=1, write_timeout=2)

"""
def serial_port_send_file(UART: Serial, file: _io):
    num_bytes = file.__sizeof__()
    UART.write(file, num_bytes)
    
    pass

"""


def serial_port_send_command(ser: Serial, data: str):
    """
    this function is used to transmit commands through serial port,
    it includes mechanism which encodes data as ASCII (bytes, b encoding)
    """

    transmit = data.encode(encoding="ascii")

    ser.write(transmit)


def serial_port_read_bytes(ser: Serial, app_element: PySimpleGUI.Multiline, num_bytes: int):

    app_element.print(ser.read(num_bytes))


def serial_port_read_to_file(ser: Serial, file: BinaryIO, num_bytes: int):
    """
        to add format of file
        """
    num_bytes_read = file.write(ser.read(num_bytes))
    file.write(bytes('\n'.encode(encoding="ascii")))

