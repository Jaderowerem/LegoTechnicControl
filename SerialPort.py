import PySimpleGUI
from serial import *
from typing import BinaryIO

uart = {
    "Device A": Serial(bytesize=EIGHTBITS, timeout=1, write_timeout=2),  # device A
    "Device B": Serial(bytesize=EIGHTBITS, timeout=1, write_timeout=2)  # device B
}


def serial_port_send_file(ser: Serial, file: BinaryIO):
    pass


def serial_port_send_command(ser: Serial, data: str):
    """
    this function is used to transmit commands through serial port,
    it includes mechanism which encodes data as ASCII (bytes, b encoding)
    """

    if ser.isOpen():

        ser.reset_output_buffer()
        transmit = data.encode(encoding="ascii")
        ser.write(transmit)

    else:

        pass


def serial_port_read_to_window(ser: Serial, app_element: PySimpleGUI.Multiline, num_bytes: int):

    if ser.isOpen():

        """
        app_element.print(ser.read(num_bytes))

        """
        if ser.isOpen():
            m = str(ser.read(num_bytes), "UTF-8")
            app_element.print(m)
            ser.reset_input_buffer()
            
            # m = ser.read(num_bytes)
            # app_element.print(m.decode("UTF-8"))

    else:

        pass


def serial_port_read_to_file(ser: Serial, file: BinaryIO, num_bytes: int):
    """
        to add format of file
        """
    if ser.isOpen():

        num_bytes_read = file.write(ser.read(num_bytes))
        file.write(bytes('\n'.encode(encoding="ascii")))

    else:

        pass
