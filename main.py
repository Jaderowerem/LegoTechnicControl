import PySimpleGUI

from Settings import *  # include all namespace from Settings.py file
from Tools import *  # import everything
from Help import *
import PySimpleGUI as sg

myProjectVersion = "0.1.11"


def RunApp():
    """
    RunApp is the main process of the GUI application, here other components
    will be added
    """

    f = 1  # the flag purpose is to protect before file closing if the file has not been created yet!

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
    app_serial_port_tab_overwrite_file = sg.Button("File overwrite", size=(16, 2), pad=(8, 0))
    app_serial_port_tab_append_file = sg.Button("Append file", size=(13, 2), pad=(0, 0))

    app_serial_port_tab_command = sg.Multiline(default_text=" Hello", key="-SERIAL_PORT_SEND_COMMAND-", size=(60, 5))
    app_serial_port_tab_send_command = sg.Button("Send command", size=(14, 2), pad=(8, 0))

    app_serial_port_tab_layout = [[app_serial_port_tab_file_to_send, app_serial_port_tab_send_file],
                                  [app_serial_port_tab_command, app_serial_port_tab_send_command],
                                  [app_serial_port_tab_read_to_file, app_serial_port_tab_overwrite_file,
                                   app_serial_port_tab_append_file]]

    app_serial_port_tab = sg.Tab("Serial port", layout=app_serial_port_tab_layout, key="-SERIAL_PORT-")

    layout_tabs = [     # layout of group of tabs
        [app_serial_port_tab]
    ]

    app_tab_group = sg.TabGroup(layout_tabs)    # create tab group object which includes all tabs

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

        app_window_display.print("event: ", event)
        app_window_display.print("values: ", values)

        if event == 'About':
            app_window.disappear()
            sg.popup('LEGO Technic PC control', myProjectVersion,
                     'based on PySimpleGUI version: ', sg.version, grab_anywhere=True)

            app_window.reappear()

        elif event == 'Open file':
            filename = sg.popup_get_file('file to open', no_window=True)

            try:

                file = open(filename, 'w')

            except OSError:

                app_window_display.print("Something went wrong during opening file")

            else:

                file.write("test writing")
                f = 0

        elif event == 'Clear display':

            app_window['-OUT-'].update('')  # clear app_window

        elif event == 'Settings':
            settings_tab()

        elif event == "Send command":

            serial_port_send_command(uart, "Test data")      # Test write

    if f == 0:  # close file which exists

        file.close()

    app_window.close()
    del app_window


RunApp()
uart.close()  # when main program was finished and port was not closed, close it
del uart


