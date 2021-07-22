from SerialPort import *
import PySimpleGUI as sg


def serial_port_config(gui_event: tuple, gui_values: tuple, window: PySimpleGUI.Window,
                       text_output: PySimpleGUI.Multiline):

    com_port = ''.join(gui_values[0])  # converts tuple or list into string
    baud = ''.join(gui_values[1])  # converts tuple or list into string
    device = ''.join(gui_values[2])  # converts tuple or list into string

    if gui_event == 'OPEN PORT':

        if uart[device].isOpen():  # if port is already opened, do not try to open it once again

            if uart[device].port == com_port:  # when selected setting covers port which is already opened

                window['settings window'].update('')
                text_output.print("The port is already opened")

            else:  # when other port is already opened, and someone is trying to open another one

                window['settings window'].update('')  # clear window
                text_output.print(uart[device].port, "is already opened, do not try to open another port")

        else:  # the port is not under usage, it can be opened

            uart[device].port = com_port
            uart[device].baudrate = int(baud)  # convert string into number

            try:  # the code which may raise exception SerialException
                uart[device].open()

            except SerialException:  # if SerialException will occur, do the management action

                window['settings window'].update('')  # clear window
                text_output.print("Something went wrong... \n The port cannot be opened")

            else:  # otherwise, inform that everything went along nicely

                window['settings window'].update('')  # clear window
                text_output.print("The port has been successfully opened")

    if gui_event == 'CLOSE PORT':

        if uart[device].isOpen():

            uart[device].close()
            window['settings window'].update('')
            text_output.print(uart[device].port, " has just been closed")

        else:

            window['settings window'].update('')
            text_output.print("It's difficult to close port which is not even opened ... :(")

    if gui_event == "READ SETTINGS":

        if uart[device].isOpen():
            window['settings window'].update('')
            text_output.print(device, ">> Port: ", uart[device].port, ", Baud rate: ", uart[device].baudrate,
                              ", Data bits: ", uart[device].bytesize, ", Parity: ", uart[device].parity, ", Stop bits: "
                              , uart[device].stopbits, ", Timeout [sec] : ", uart[device].timeout)
        else:

            window['settings window'].update('')
            text_output.print("No port is currently opened")


def settings_tab():
    settings_com_ports = ['COM0', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7',
                          'COM8', 'COM9', 'COM10', 'COM11', 'COM12', 'COM13', 'COM14',
                          'COM15', 'COM16', 'COM17', 'COM18', 'COM19']

    settings_baudrate = ['9600', '14400', '19200', '38400', '57600', '115200']

    settings_devices = ["Device A", "Device B"]

    settings_output = sg.Multiline(key='settings window', size=(50, 2))

    settings_serial_port_layout = [[sg.Text('Serial ports', pad=(10, 0)), sg.Text('Baud rate', pad=(20, 10)),
                                    sg.Text('Device', pad=(20, 10))],
                                   [sg.Listbox(settings_com_ports, default_values=['COM0'], size=(7, 5),
                                               enable_events=True, pad=(10, 10)),
                                    sg.Listbox(settings_baudrate, default_values=['9600'], size=(7, 5),
                                               enable_events=True, pad=(20, 10)),
                                    sg.Listbox(settings_devices, default_values=["Device A"], size=(9, 3),
                                               enable_events=True, pad=((10, 10), (0, 30)))],
                                   [sg.Button('OPEN PORT', pad=(10, 20)), sg.Button('CLOSE PORT', pad=(0, 20)),
                                    sg.Button("READ SETTINGS", pad=(10, 0))],
                                   [settings_output]]

    settings_serial_port_tab = sg.Tab("Serial port", layout=settings_serial_port_layout)

    settings_font_layout = [[]]
    settings_font_tab = sg.Tab("Font & text", layout=settings_font_layout)

    settings_theme_layout = [[]]
    settings_theme_tab = sg.Tab("Theme", layout=settings_theme_layout)

    layout_tabs = [
        [settings_serial_port_tab],
        [settings_font_tab],
        [settings_theme_tab]
    ]

    settings_tab_group = sg.TabGroup(layout_tabs)

    settings_layout = [
        [settings_tab_group]
    ]

    settings_window = sg.Window('Settings', layout=settings_layout)

    while True:

        settings_event, settings_values = settings_window.read()

        if settings_event in (sg.WIN_CLOSED, 'Exit'):
            break

        else:

            serial_port_config(settings_event, settings_values, settings_window, settings_output)

    settings_window.close()
    del settings_window  # destructor, deletes setting_window object
    del settings_output
    del settings_layout
