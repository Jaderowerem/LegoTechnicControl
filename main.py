import PySimpleGUI
import time

from Settings import *  # include all namespace from Settings.py file
from Tools import *  # from Tools import everything
from Help import *  # from Help import everything
from Zigbee import *    # from Zigbee import everything
import PySimpleGUI as sg

myProjectVersion = "0.2.2"


def runApp():
    """
    RunApp is the main process of the GUI application, here other components
    will be added
    """
    sg.theme('Dark')
    sg.set_options(element_padding=(0, 0))

    # ------ Menu Definition ------ #
    menu_def = [['&File', ['Clear window', 'Settings', 'Exit']],
                ['&View'],
                ['&Toolbar', ['none', 'none', 'none']],
                ['&Help', '&About', '&Manual'], ]

    # ------ GUI Definition ------ #
    """
    use Multiline objects instead of Output, it resolves problem regarding print() in built function
    when more than one Window object is being used
    """
    app_main_menu = sg.Menu(menu_def, tearoff=False, pad=(200, 1), key='-MAIN_MENU-')
    app_window_receive_text = sg.Text("Receive window", pad=(0, 5))
    app_window_receive = sg.Multiline(key='-RECEIVE-', size=(60, 6))
    app_window_transmit_text = sg.Text("Send window", pad=(0, 5))
    app_window_transmit = sg.Multiline(key='-TRANSMIT-', size=(60, 1), pad=(0, 0))

    """
    Creating tab, elements inside tab and setting layout
    
        1. Create objects of GUI using template app_module name_tab_option
        2. Create nested list as app_module name_tab_layout object to store layout
        3. Create tab app_module name_tab object using previously created layout
        4. Add the tab into layout_tabs object
    """

    """
    1.
    """
    app_serial_port_tab_file_section = sg.Text(" File ", pad=(0, 10))
    app_serial_port_tab_file_to_send = sg.Button("FILE TO SEND", size=(14, 1), pad=(10, 10))
    app_serial_port_tab_send_file = sg.Button("SEND FILE", size=(12, 1), pad=(10, 0))
    app_serial_port_tab_file_to_record = sg.Button("FILE TO RECORD DATA", size=(22, 1), pad=(0, 0))
    app_serial_port_tab_read_to_file = sg.Button("READ TO FILE", size=(14, 1), pad=(0, 0))
    app_serial_port_tab_close_file = sg.Button("CLOSE FILE", size=(15, 1), pad=(10, 0))
    app_serial_port_tab_message_section = sg.Text(" Message ", pad=(0, 10))
    app_serial_port_tab_send_message = sg.Button("SEND", size=(12, 1), pad=(10, 0), key="SEND")
    # key defines name of events and values (key of dictionary)
    app_serial_port_tab_read = sg.Button("READ", size=(12, 1), pad=(0, 0))
    app_serial_port_tab_devices_section = sg.Text(" Device ", pad=(220, 10))

    app_serial_port_devices = ["Device A", "Device B"]

    app_serial_port_tab_devices = sg.Listbox(app_serial_port_devices, default_values=["Device A"], size=(9, 3),
                                             enable_events=True, pad=((40, 10), (20, 0)))

    zigbee_serial_ports = ['COM0', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7',
                           'COM8', 'COM9', 'COM10', 'COM11', 'COM12', 'COM13', 'COM14',
                           'COM15', 'COM16', 'COM17', 'COM18', 'COM19']

    zigbee_baudrate = ['9600', '14400', '19200', '38400', '57600', '115200']

    zigbee_signal_channel = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
                             '22', '23', '24', '25', '26']

    app_zigbee_tab_serial_channel = sg.Listbox(zigbee_serial_ports, default_values=['COM0'], size=(7, 5),
                                               enable_events=True, key="ZIGBEE_SETTING_PORT", pad=(10, 0))

    app_zigbee_tab_serial_baudrate = sg.Listbox(zigbee_baudrate, default_values=['9600'], size=(7, 5),
                                                enable_events=True, key="ZIGBEE_SETTING_BAUDRATE", pad=(20, 0))

    app_zigbee_tab_signal_channel = sg.Listbox(zigbee_signal_channel, default_values=['11'], size=(7, 5),
                                               enable_events=True, key="ZIGBEE_SETTING_CHANNEL", pad=(10, 0))

    app_zigbee_tab_panid_input = sg.Input(key='ZIGBEE_SET_PANID', size=(10, 1), pad=((40, 0), (0, 60)))

    app_zigbee_button_menu_commands = ["UNUSED", ["RESTART MODULE", "SET FACTORY SETTINGS", "SET SERIAL PORT",
                                                  "SET SIGNAL CHANNEL", "SET PANID", "GET CONFIGURATION",
                                                  "GET SERIAL PORT", "GET SIGNAL CHANNEL", "GET PANID",
                                                  "GET SHORT ADDRESS OF THE DEVICE", "GET SHORT PARENT ADDRESS",
                                                  "GET DEVICE IEEE ADDRESS", "GET PARENT IEEE ADDRESS"
                                                  ]]

    app_zigbee_tab_commands = sg.ButtonMenu("ZigBee command", menu_def=app_zigbee_button_menu_commands,
                                            pad=(10, 0), key="ZIGBEE_COMMAND")

    app_zigbee_tab_send_commands = sg.Button("SEND", pad=(10, 0), key="ZIGBEE_MANUAL_SEND")

    app_zigbee_devices = ["Device A", "Device B"]

    app_zigbee_tab_devices = sg.Listbox(app_zigbee_devices, default_values=["Device A"], size=(9, 3),
                                        enable_events=True, pad=((110, 0), (0, 20)))

    app_zigbee_tab_serial_channel_section = sg.Text(" Serial channel ", pad=(0, 10))
    app_zigbee_tab_serial_baudrate_section = sg.Text(" Baud rate ", pad=(20, 10))
    app_zigbee_tab_signal_channel_section = sg.Text(" Signal channel ", pad=(0, 0))
    app_zigbee_tab_signal_panid_section = sg.Text(" PANID ", pad=(30, 0))
    app_zigbee_tab_signal_panid_info = sg.Text(" Set address 0x0000 - 0x3FFE ", pad=((0, 0), (0, 60)))
    app_zigbee_tab_commands_section = sg.Text(" Commands ", pad=(0, 20))
    app_zigbee_tab_devices_section = sg.Text(" Device ", pad=((280, 0), (0, 0)))

    """
    2.
    """
    app_serial_port_tab_layout = [[app_serial_port_tab_file_section],
                                  [app_serial_port_tab_file_to_send, app_serial_port_tab_file_to_record,
                                   app_serial_port_tab_send_file, app_serial_port_tab_read_to_file,
                                   app_serial_port_tab_close_file],
                                  [app_serial_port_tab_message_section, app_serial_port_tab_devices_section],
                                  [app_serial_port_tab_send_message, app_serial_port_tab_read,
                                   app_serial_port_tab_devices],
                                  ]

    app_zigbee_tab_layout = [[app_zigbee_tab_serial_channel_section, app_zigbee_tab_serial_baudrate_section,
                              app_zigbee_tab_signal_channel_section,
                              app_zigbee_tab_signal_panid_section],
                             [app_zigbee_tab_serial_channel, app_zigbee_tab_serial_baudrate,
                              app_zigbee_tab_signal_channel, app_zigbee_tab_panid_input,
                              app_zigbee_tab_signal_panid_info], [app_zigbee_tab_commands_section,
                                                                  app_zigbee_tab_devices_section],
                             [app_zigbee_tab_commands, app_zigbee_tab_send_commands,
                              app_zigbee_tab_devices]]
    """
    3.
    """
    app_serial_port_tab = sg.Tab(" Serial port ", layout=app_serial_port_tab_layout, key="-SERIAL_PORT-")

    app_zigbee_tab = sg.Tab(" Zigbee ", layout=app_zigbee_tab_layout, key="-ZIGBEE_TAB-", pad=(0, 20))

    """
    4.
    """
    layout_tabs = [  # layout of group of tabs
        [app_serial_port_tab],
        [app_zigbee_tab]
    ]

    app_tab_group = sg.TabGroup(layout_tabs)  # create tab group object which includes all tabs

    app_main_layout = [
        [app_main_menu],
        [app_window_receive_text],
        [app_window_receive],
        [app_window_transmit_text],
        [app_window_transmit],
        [app_tab_group]
    ]
    """
    Create main window object
    """
    app_window = sg.Window('LEGO Technic PC control',
                           app_main_layout,
                           default_element_size=(12, 1),
                           default_button_element_size=(12, 1), size=(800, 600))

    # ------ Loop & Process button menu choices ------ #
    while True:

        event, values = app_window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        # ------ Process menu choices ------ #

        """
        app_window_receive.print() use only to debug UI when other features are disabled like
        for example data transmission via UART, etc, otherwise application is going to work unstable
        """
        # app_window_receive.print("event: ", event)  # debug
        # app_window_receive.print("values: ", values) # debug

        device = ''.join(values[0])     # converts tuple or list into string, get proper device- A or B

        if event == 'About':
            app_window.disappear()
            sg.popup('LEGO Technic PC control', myProjectVersion,
                     'based on PySimpleGUI version: ', sg.version, grab_anywhere=True)

            app_window.reappear()

        elif event == 'Clear window':

            app_window['-RECEIVE-'].update('')  # clear app_window

        elif event == 'Settings':
            settings_tab()

        elif event == "SEND":

            txd_data = app_window_transmit.get()
            serial_port_send_command(uart[device], txd_data)

        elif event == "FILE TO RECORD DATA":

            file_read_uart_name = sg.popup_get_file('File to open', no_window=True)

            try:

                file_read_uart = open(file_read_uart_name, 'wb')

            except OSError:

                app_window_receive.print("The file cannot be opened")

        elif event == "READ TO FILE":

            serial_port_read_to_file(uart[device], file_read_uart, txd_data.__sizeof__())
            pass

        elif event == "READ":

            serial_port_read_bytes(uart[device], app_window_receive, txd_data.__sizeof__())
            pass

        elif event == "CLOSE FILE":

            file_read_uart.close()

        elif event == "ZIGBEE_COMMAND":

            get_zigbee_command(event, values, app_window_transmit)

        elif event == "ZIGBEE_MANUAL_SEND":

            txd_data = app_window_transmit.get()
            serial_port_send_command(uart[device], txd_data)

    app_window.close()
    del app_window


runApp()

if uart["Device A"].isOpen():

    uart["Device A"].close()  # when main program was finished and port was not closed, close it
    del uart["Device A"]

if uart["Device B"].isOpen():

    uart["Device B"].close()  # when main program was finished and port was not closed, close it
    del uart["Device B"]



