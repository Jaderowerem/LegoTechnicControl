import PySimpleGUI

from Settings import *
from SerialPort import *

CRC8_lookuptable = []  # a global list which will store generated CRC-8

"""
MySimpleProtocol exceptions definition
"""


class MySimpleProtocolDataLength(Exception):
    """
    Raised when received number of bytes is not proper
    """
    pass


class MySimpleProtocolCRC8(Exception):
    """
    Raised when calculated CRC-8 is not equal to received CRC-8
    """
    pass


class MySimpleProtocolStatus(Exception):
    """
    Raised when NOK status has been received
    """
    pass


class MySimpleProtocolGeneral(Exception):
    """
    Raised when NOK status has been received
    """
    pass


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

    result_crc = str(crc)
    if len(result_crc) < 3:  # if length of CRC-8 is less than 3 characters, add 0 at the beginning
        result_crc = "0" + result_crc

    return result_crc


def get_length_of_data(data: str):
    return len(data)


def MySimpleProtocol_transmit(data: str, transmission_type: str, destination_addr: str, source_addr: str,
                              uart_device: str):
    """
    MySimpleProtocol ver 1.0 is simple protocol used to transmit and receive data between modules in Zigbee network
    using P2P txd_packet

    Where at least one module should be configured as transmitter (for example coordinator, server),
    other devices as receivers by default

    :param data: data to be transmitted, string characters
    :param transmission_type: a type of transmission:
        - CTRL - control
        - PROG - programming
        - READ - readout

    :param destination_addr: address of destination ZigBee module
    :param source_addr: sender address
    :param uart_device: indicates which uart device is being used: Device A or B
    :return:

        1) A -> B: Transmit first txd_packet which includes total number of data characters (bytes) and indicates
        a type of transmission

        Start transmission packet: P2P address_B_module sender_address transmission_type data_length CRC-8

        sender_address is encoded by 4B (support for multiple ZigBee modules in network)
        transmission_type is encoded using 4B
        data_length is encoded using 3 characters of ASCII code
        data_length = ASCII characters used to encode object name + ASCII characters to encode value + 2 (space signs)

        The role of space sign is a separator

        CRC-8 is encoded using 3 characters of ASCII code

        Total number of bytes to be transmitted is 17
        (4B [sender address] + 1B [space] + 4B [transmission type] + 1B [space] +
        3B [Data length] + 1B [space] + 3B [CRC-8])

        2) module B computes CRC-8, if computed CRC-8 covers received CRC, B sends confirmation message OK_
        otherwise, NOK message will be transmitted and the transmission is treated as not valid !!!

        Transmission status:
        OK_ - transmission is valid (3 ASCII characters)
        NOK - transmission is not valid (3 ASCII characters)
        BSY - busy status, sent when the module is processing currently other transmission

        txd_packet to receive is: sender_address status CRC-8

        Total number of bytes to receive is 12 (4B [sender address] + 1B [space] +
        3B [status] + 1B [space] + 3B [CRC-8]

        3) If transmission is valid, A-> B sends object name and value

        P2P address_B_module sender_address object_name value CRC-8

        4) exactly the same procedure like in step 2)

    For each step, CRC-8 is computed including space signs !!!
    However, first ZigBee header (P2P Address) is not taken into consideration
    because it is not visible by this layer when data are being received via UART
    """

    """
    1)  Send Start transmission packet to inform receiver about transmission type and following 
    number of bytes to receive for data field
    """
    Data_length = get_length_of_data(data)
    Encoded_Data_length = ""

    if Data_length < 10:
        Encoded_Data_length = "00" + str(Data_length)  # if there is 1 character, add 00 at the beginning

    elif Data_length < 100:
        Encoded_Data_length = "0" + str(Data_length)  # if there are 2 characters, add 0 at the beginning

    elif Data_length >= 100:
        Encoded_Data_length = str(Data_length)  # max 999 B can be transmitted !!!

    if transmission_type == "CTRL":
        txd_packet = source_addr + " " + "CTRL" + " " + Encoded_Data_length + " "
        """
        CRC does not include P2P Address_ZigBee_module because these elements
        are not visible for data readout via UART- received bytes from UART does
        not contain ZigBee header
        """
        packet_CRC8 = Compute_CRC8(txd_packet, CRC8_lookuptable, 0)

        # now add P2P Address_ZigBee_module at the beginning of the txd_packet

        txd_packet = "P2P " + destination_addr + " " + txd_packet + packet_CRC8

        print("length of the txd_packet without ZigBee header: ", len(txd_packet[9::]),
              "B", ", packet: ", txd_packet)  # debug

        # Send txd_packet via UART to ZigBee module
        serial_port_send_command(uart[uart_device], txd_packet)

    """
    2)  Check feedback from receiver
    """
    rxd_packet = ""  # create buffer for readout
    """
    start loop
    """
    while True:
        serial_port_read_to_buffer(uart[uart_device], rxd_packet, 12)

        if len(rxd_packet) != 12:

            raise MySimpleProtocolDataLength  # raise exception when received number of bytes is not
            # equal to 12

        else:  # go on
            packet_CRC8 = Compute_CRC8(rxd_packet[0:9], CRC8_lookuptable, 0)

            if packet_CRC8 != rxd_packet[9::]:
                """
                Before raising exception, check if something is trying to start a new transmission during 
                lasting transmission - device is busy
                """
                rxd_reg = rxd_packet  # save receive buffer content

                # receive reaming bytes to check if Start transmission packet came
                serial_port_read_to_buffer(uart[uart_device], rxd_packet, 5)
                rxd_packet = rxd_reg + rxd_packet  # build the packet

                # compute CRC- 8 for Start transmission packet
                packet_CRC8 = Compute_CRC8(rxd_packet[0:14], CRC8_lookuptable, 0)
                if packet_CRC8 != rxd_packet[14::]:
                    # raise exception when calculated CRC-8 does not cover received one
                    raise MySimpleProtocolCRC8

                else:
                    wait_module_addr = rxd_packet[0:4]

                    if destination_addr != wait_module_addr:
                        # it indicates that other module is trying to start transmission

                        # send BSY status to module which is trying to start transmission
                        txd_packet = source_addr + " " + "BSY "
                        packet_CRC8 = Compute_CRC8(txd_packet, CRC8_lookuptable, 0)
                        txd_packet = "P2P " + wait_module_addr + " " + txd_packet + packet_CRC8
                        serial_port_send_command(uart[uart_device], txd_packet)

                    else:
                        raise MySimpleProtocolGeneral

            else:  # go on
                break  # exit the loop

    status = rxd_packet[5:8]

    if status == "NOK":
        raise MySimpleProtocolStatus  # raise the exception when no OK_ status has been received

    elif status == "BSY":
        return "Destination module is busy"  # if module is processing currently other transmission

    elif status != "NOK" or status != "BSY" or status != "OK_":
        raise MySimpleProtocolStatus  # raise the exception when no supported status has been
        # received

    elif status == "OK_":
        """
        3)  Go on transmission if it is still valid
        """
        # transmission is valid, go on
        txd_packet = source_addr + " " + data + " "
        packet_CRC8 = Compute_CRC8(txd_packet, CRC8_lookuptable, 0)  # calculate CRC-8 for data
        # prepare packet
        txd_packet = "P2P " + destination_addr + " " + txd_packet + packet_CRC8
        # Send txd_packet via UART to ZigBee module
        serial_port_send_command(uart[uart_device], txd_packet)

        """
        4)  Check feedback from receiver, if CRC-8 and status will be fine, transmission ends up and is valid
        """
        while True:
            serial_port_read_to_buffer(uart[uart_device], rxd_packet, 12)

            if len(rxd_packet) != 12:

                raise MySimpleProtocolDataLength  # raise exception when received number of bytes is not
                # equal to 12

            else:  # go on
                packet_CRC8 = Compute_CRC8(rxd_packet[0:9], CRC8_lookuptable, 0)

                if packet_CRC8 != rxd_packet[9::]:
                    """
                    Before raising exception, check if something is trying to start a new transmission during 
                    lasting transmission - device is busy
                    """
                    rxd_reg = rxd_packet  # save receive buffer content

                    # receive reaming bytes to check if Start transmission packet came
                    serial_port_read_to_buffer(uart[uart_device], rxd_packet, 5)
                    rxd_packet = rxd_reg + rxd_packet  # build the packet

                    # compute CRC- 8 for Start transmission packet
                    packet_CRC8 = Compute_CRC8(rxd_packet[0:14], CRC8_lookuptable, 0)
                    if packet_CRC8 != rxd_packet[14::]:
                        # raise exception when calculated CRC-8 does not cover received one
                        raise MySimpleProtocolCRC8

                    else:
                        wait_module_addr = rxd_packet[0:4]

                        if destination_addr != wait_module_addr:
                            # it indicates that other module is trying to start transmission

                            # send BSY status to module which is trying to start transmission
                            txd_packet = source_addr + " " + "BSY "
                            packet_CRC8 = Compute_CRC8(txd_packet, CRC8_lookuptable, 0)
                            txd_packet = "P2P " + wait_module_addr + " " + txd_packet + packet_CRC8
                            serial_port_send_command(uart[uart_device], txd_packet)

                        else:
                            raise MySimpleProtocolGeneral

                else:  # go on
                    break  # exit the loop

        status = rxd_packet[5:8]

        if status == "NOK":
            raise MySimpleProtocolStatus  # raise the exception when no OK_ status has been received

        elif status == "BSY":
            return "Destination module is busy"  # if module is processing currently other transmission

        elif status != "NOK" or status != "BSY" or status != "OK_":
            raise MySimpleProtocolStatus  # raise the exception when no supported status has been
            # received

        elif status == "OK_":
            return "Valid transmission"  # transmission successfully ends up


def MySimpleProtocol_receive(data: str, transmission_type: str, Address_ZigBee_module: str, uart_device: str):
    pass
