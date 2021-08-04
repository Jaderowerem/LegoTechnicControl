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
    "PACKET FROM MODULE B TO A": "P2P "  # adding space to differ packets between sending from A to B and from B to A
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

        panid = "".join(gui_values["ZIGBEE_SET_PANID"])  # convert list into string
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
        command = command + addrAmodule + " "  # there is no need to add space sign because it was used to differ
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


def Compute_CRC8(data: str, lookUpTable: list, initial_crc: int):
    """
    :param data: input data, by default set to 0
    :param lookUpTable: look up table which stores computed CRC 8 values
    for given polynomial, it should be global object
    :param initial_crc: initial value of CRC
    :return: computed CRC-8
    for input data
    """

    crc = initial_crc

    for str_char in data:
        dec_char = ord(str_char)  # convert string character into decimal value 0 - 255
        xor_in = dec_char ^ crc
        crc = lookUpTable[xor_in]

    return str(crc)


def get_length_of_data(data: str):

    return len(data)


def MySimpleProtocol_transmit(data: str):

    """
    MySimpleProtocol ver 1.0 is simple protocol used to transmit and receive data between modules in Zigbee network
    using P2P packet

    :param data: data to be transmitted, string characters
    :return:

        1) A -> B: Transmit first packet which includes total number of data characters (bytes)

        P2P address_B_module data_length CRC-8

        data_length is encoded using 3 characters of ASCII code
        data_length = ASCII characters used to encode object name + ASCII characters to encode value + 2 (space signs)

        The role of space sign is a separator

        CRC-8 is encoded using 3 characters of ASCII code

        Total number of bytes to be transmitted is 7 (3 + 3 + space sign between data_length and CRC-8)

        2) module B computes CRC-8, if computed CRC-8 covers received CRC, B sends confirmation message OK_
        otherwise, NOK message will be transmitted and the transmission is treated as not valid !!!

        Transmission status:
        OK_ - transmission is valid (3 ASCII characters)
        NOK - transmission is not valid (3 ASCII characters)

        packet to receive is: status CRC-8

        Total number of bytes to receive is 7 (3 + 1 (space) + 3 (CRC-8))

        3) If transmission is valid, A-> B sends object name and value

        P2P address_B_module object_name value CRC-8

        4) exactly the same procedure like in step 2)

    For each step, CRC-8 is computed including space signs !!!
    However, P2P address is not taken into consideration for CRC-8 (it is not visible for this layer)
    """
    txd_data = data + " "   # add space sign
    Data_length = get_length_of_data(txd_data)

    if Data_length < 100:
        Encoded_Data_length = "0" + str(Data_length)    # if there are 2 characters, add 0 at the beginning

    else:
        Encoded_Data_length = str(Data_length)

    Compute_CRC8(Encoded_Data_length, )



