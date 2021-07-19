import PySimpleGUI
import time

from Settings import *  # include all namespace from Settings.py file
from Tools import *  # import everything
from Help import *
import PySimpleGUI as sg


myProjectVersion = "0.1.17"


def RunApp():
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

    app_serial_port_tab_file_section = sg.Text(" File ", pad=(0, 10))
    app_serial_port_tab_file_to_send = sg.Button("FILE TO SEND", size=(14, 2), pad=(10, 10))
    app_serial_port_tab_send_file = sg.Button("SEND FILE", size=(12, 2), pad=(10, 0))
    app_serial_port_tab_file_to_record = sg.Button("FILE TO RECORD DATA", size=(22, 2), pad=(0, 0))
    app_serial_port_tab_read_to_file = sg.Button("READ TO FILE", size=(14, 2), pad=(0, 0))
    app_serial_port_tab_close_file = sg.Button("CLOSE FILE", size=(12, 2), pad=(10, 0))

    app_serial_port_tab_messgae_section = sg.Text(" Message ", pad=(0, 10))
    app_serial_port_tab_send_message = sg.Button("SEND", size=(12, 2), pad=(10, 0))
    app_serial_port_tab_read = sg.Button("READ", size=(12, 2), pad=(0, 0))

    app_serial_port_tab_layout = [[app_serial_port_tab_file_section ], [app_serial_port_tab_file_to_send, app_serial_port_tab_file_to_record,
                                app_serial_port_tab_send_file, app_serial_port_tab_read_to_file, app_serial_port_tab_close_file],
                                [app_serial_port_tab_messgae_section], [app_serial_port_tab_send_message, app_serial_port_tab_read],
                                ]

    app_serial_port_tab = sg.Tab(" Serial port ", layout=app_serial_port_tab_layout, key="-SERIAL_PORT-")

    app_zigbee_tab_layout = [[]]

    app_zigbee_tab = sg.Tab(" Zigbee ", layout=app_zigbee_tab_layout, key="-ZIGBEE-", pad=(0, 20))

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

    app_window = sg.Window('LEGO Technic PC control',
                           app_main_layout,
                           default_element_size=(12, 1),
                           default_button_element_size=(12, 1), size=(1000, 600))

    # ------ Loop & Process button menu choices ------ #
    while True:

        event, values = app_window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        # ------ Process menu choices ------ #

        """
        app_window_receive.print() use only to debug UI when other features are disabled like
        for example data transmission via UART, etc, otherwise application is goiing to work unstable
        """
        # app_window_receive.print("event: ", event)  # debug
        # app_window_receive.print("values: ", values) # debug

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
            serial_port_send_command(uart, txd_data)

        elif event == "FILE TO RECORD DATA":

            file_read_uart_name = sg.popup_get_file('File to open', no_window=True)

            try:

                file_read_uart = open(file_read_uart_name, 'wb')

            except OSError:

                app_window_receive.print("The file cannot be opened")

        elif event == "READ TO FILE":

            serial_port_read_to_file(uart, file_read_uart, txd_data.__sizeof__())

        elif event == "READ":

            serial_port_read_bytes(uart, app_window_receive, txd_data.__sizeof__())

        elif event == "CLOSE FILE":

            file_read_uart.close()

    app_window.close()
    del app_window

RunApp()
uart.close()  # when main program was finished and port was not closed, close it
del uart

