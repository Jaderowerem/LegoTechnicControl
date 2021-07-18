import PySimpleGUI
import time

from Settings import *  # include all namespace from Settings.py file
from Tools import *  # import everything
from Help import *
import PySimpleGUI as sg


myProjectVersion = "0.1.15"


def RunApp():
    """
    RunApp is the main process of the GUI application, here other components
    will be added
    """
    sg.theme('Dark')
    sg.set_options(element_padding=(0, 0))

    # ------ Menu Definition ------ #
    menu_def = [['&File', ['Open file', 'Clear display', 'Settings', 'Exit']],
                ['&Edit', ['&Paste', ['None']], ],
                ['&View'],
                ['&Toolbar', ['DebugTool', 'MonitorTool', 'None']],
                ['&Help', '&About', '&Manual'], ]

    # ------ GUI Definition ------ #
    """
    use Multiline objects instead of Output, it resolves problem regarding print() in built function
    when more than one Window object is being used
    """
    app_main_menu = sg.Menu(menu_def, tearoff=False, pad=(200, 1), key='-MAIN_MENU-')
    app_window_display = sg.Multiline(key='-OUT-', size=(80, 7))

    app_serial_port_tab_file_to_send = sg.Button("Load file to send", size=(19, 2), pad=(0, 10))
    app_serial_port_tab_send_file = sg.Button("Send file", size=(11, 2), pad=(8, 0))

    app_serial_port_tab_read_to_file = sg.Button("Load file to read data", size=(24, 2), pad=(0, 10))
    app_serial_port_tab_close_file = sg.Button("Close file", size=(16, 2), pad=(0, 0))
    app_serial_port_tab_read_data = sg.Button("Read data", size=(13, 2), pad=(8, 0))

    app_serial_port_tab_command_input = sg.Multiline(default_text=" Hello", key="-SERIAL_PORT_SEND_COMMAND-",
                                                     size=(60, 1))
    app_serial_port_tab_send_command = sg.Button("Send command", size=(14, 2), pad=(8, 0))

    app_serial_port_tab_layout = [[app_serial_port_tab_file_to_send, app_serial_port_tab_send_file],
                                  [app_serial_port_tab_command_input, app_serial_port_tab_send_command],
                                  [app_serial_port_tab_read_to_file, app_serial_port_tab_read_data,
                                   app_serial_port_tab_close_file]]

    app_serial_port_tab = sg.Tab("Serial port", layout=app_serial_port_tab_layout, key="-SERIAL_PORT-")

    layout_tabs = [  # layout of group of tabs
        [app_serial_port_tab]
    ]

    app_tab_group = sg.TabGroup(layout_tabs)  # create tab group object which includes all tabs

    app_main_layout = [
        [app_main_menu],
        [app_window_display],
        [app_tab_group]
    ]

    app_window = sg.Window('LEGO Technic PC control',
                           app_main_layout,
                           default_element_size=(12, 1),
                           default_button_element_size=(12, 1))

    # ------ Loop & Process button menu choices ------ #
    while True:

        event, values = app_window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        # ------ Process menu choices ------ #

        """
        app_window_display.print() use only to debug UI when other features are disabled like
        for example data transmission via UART, etc, otherwise application is goiing to work unstable
        """
        # app_window_display.print("event: ", event)  # debug
        # app_window_display.print("values: ", values) # debug

        if event == 'About':
            app_window.disappear()
            sg.popup('LEGO Technic PC control', myProjectVersion,
                     'based on PySimpleGUI version: ', sg.version, grab_anywhere=True)

            app_window.reappear()

        elif event == 'Open file':
            filename = sg.popup_get_file('file to open', no_window=True)

        elif event == 'Clear display':

            app_window['-OUT-'].update('')  # clear app_window

        elif event == 'Settings':
            settings_tab()

        elif event == "Send command":

            txd_data = app_serial_port_tab_command_input.get()
            serial_port_send_command(uart, txd_data)

            """
            test
            """
            serial_port_read_to_file(uart, file_read_uart, txd_data.__sizeof__())

        elif event == "Load file to read data":

            file_read_uart_name = sg.popup_get_file('file to open', no_window=True)

            try:

                file_read_uart = open(file_read_uart_name, 'wb')

            except OSError:

                app_window_display.print("The file cannot be opened")

        elif event == "Read data":

            serial_port_read_to_file(uart, file_read_uart, txd_data.__sizeof__())

        elif event == "Close file":

            file_read_uart.close()

    app_window.close()
    del app_window
    del app_main_menu
    del app_window_display
    del app_serial_port_tab_file_to_send
    del app_serial_port_tab_send_file
    del app_serial_port_tab_read_to_file
    del app_serial_port_tab_close_file
    del app_serial_port_tab_read_data
    del app_serial_port_tab_command_input
    del app_serial_port_tab_send_command
    del app_serial_port_tab_layout
    del app_serial_port_tab
    del layout_tabs
    del app_tab_group
    del app_main_layout

RunApp()
uart.close()  # when main program was finished and port was not closed, close it
del uart

