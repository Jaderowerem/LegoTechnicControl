import PySimpleGUI

from Settings import *

"""
zigbee_commands_set is equivalent to app_zigbee_button_menu_commands in main.py
to get ZigBee command, values- it is a dictionary

>> zigbee_commands_set[values["ZIGBEE_COMMAND"]]
"""
zigbee_commands_set = {
    "RESTART MODULE": "AT+RESTART",
    "SET FACTORY SETTINGS": "AT+RESET",
    "SET SERIAL PORT": "AT+SETUART",
    "SET SIGNAL CHANNEL": "AT+SETCHN",
    "SET PANID": "AT+SETPANID",
    "GET CONFIGURATION": "AT+GETCFG",
    "GET SERIAL PORT": "AT+GETUART",
    "GET SIGNAL CHANNEL": "AT+GETCHN",
    "GET PANID": "AT+GETPANID",
    "GET SHORT ADDRESS OF THE DEVICE": "AT+GETADDR",
    "GET SHORT PARENT ADDRESS": "AT+GETFADDR",
    "GET DEVICE IEEE ADDRESS": "AT+GETIEEE",
    "GET PARENT IEEE ADDRESS": "AT+GETFIEEE",
    "PACKET FROM MODULE A TO B": "P2P",
    "PACKET FROM MODULE B TO A": "P2P "     # adding space to differ packets between sending from A to B and from B to A
}


def show_device_addr(packet: str, addr_to_show: PySimpleGUI.Input):

    addr = packet[7::]  # format of address xxxx
    addr_to_show.update(addr)


def get_zigbee_command(gui_values: tuple, text_output: PySimpleGUI.Input):
    command = zigbee_commands_set[gui_values["ZIGBEE_COMMAND"]]

    if command == zigbee_commands_set["SET FACTORY SETTINGS"]:
        text_output.update(command)

    elif command == zigbee_commands_set["RESTART MODULE"]:
        text_output.update(command)

    elif command == zigbee_commands_set["GET CONFIGURATION"]:
        text_output.update(command)

    elif command == zigbee_commands_set["GET SERIAL PORT"]:
        text_output.update(command)

    elif command == zigbee_commands_set["GET SIGNAL CHANNEL"]:
        text_output.update(command)

    elif command == zigbee_commands_set["GET PANID"]:
        text_output.update(command)

    elif command == zigbee_commands_set["GET SHORT ADDRESS OF THE DEVICE"]:
        text_output.update(command)

    elif command == zigbee_commands_set["GET SHORT PARENT ADDRESS"]:
        text_output.update(command)

    elif command == zigbee_commands_set["GET DEVICE IEEE ADDRESS"]:
        text_output.update(command)

    elif command == zigbee_commands_set["GET PARENT IEEE ADDRESS"]:
        text_output.update(command)

    elif command == zigbee_commands_set["SET SIGNAL CHANNEL"]:

        channel = "".join(gui_values["ZIGBEE_SETTING_CHANNEL"])
        command = command + " " + channel
        text_output.update(command)

    elif command == zigbee_commands_set["SET PANID"]:

        panid = "".join(gui_values["ZIGBEE_SET_PANID"])     # convert list into string
        command = command + " " + panid
        text_output.update(command)

    elif command == zigbee_commands_set["SET SERIAL PORT"]:

        pass

    elif command == zigbee_commands_set["PACKET FROM MODULE A TO B"]:

        addrBmodule = "".join(gui_values["ZIGBEE_ADDR_B"])
        command = command + " " + addrBmodule + " "
        text_output.update(command)

    elif command == zigbee_commands_set["PACKET FROM MODULE B TO A"]:

        addrAmodule = "".join(gui_values["ZIGBEE_ADDR_A"])
        command = command + addrAmodule + " "     # there is no need to add space sign because it was used to differ
        # commands
        text_output.update(command)


def Calculate_CRC8_lookUpTable(lookUpTable: list, polynomial: int, data_format: str):

    """
    :param lookUpTable: destination list object where generated look up table will be stored
    :param polynomial: CRC polynomial
    :param data_format: defines data format
        - bin - binary data presentation
        - hex - hexadecimal data format
        - decimal - by default, decimal format

    """
    for div in range(0, 256, 1):
        byte = div

        for bit in range(0, 8, 1):

            if byte & 0x80 != 0:

                byte = (byte << 1) ^ polynomial
                if byte > 255:
                    byte = byte & 0x00FF

            else:

                byte = byte << 1
                if byte > 255:
                    byte = byte & 0x00FF

        if data_format == 'bin':
            lookUpTable.append(bin(byte))

        elif data_format == 'hex':
            lookUpTable.append(hex(byte))

        else:
            lookUpTable.append(byte)


def Compute_CRC8(data: str, lookUpTable: list):

    """
    :param data: input data
    :param lookUpTable: look up table which stores computed CRC 8 values for given polynomial
    :return: computed CRC-8 for input data
    """
    crc = 0

    for i in data:
        xor_in = i ^ crc
        crc = lookUpTable[xor_in]

    return crc
