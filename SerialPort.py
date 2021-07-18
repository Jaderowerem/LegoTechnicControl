import _io
from serial import *

uart = Serial(bytesize=EIGHTBITS, timeout=1, write_timeout=2)

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

    UART.write(data.encode(encoding="ascii", errors="replace"))


def serial_port_read_bytes():
    pass


def serial_port_read_to_file(UART: Serial, file: _io.FileIO, num_bytes: int):
    """
        to add format of file
        """

    num_bytes_read = file.write(UART.read(num_bytes))
    file.write(bytes('\n'.encode(encoding="ascii")))

    print(num_bytes_read)  # debug
    print("Ready")
