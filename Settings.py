import serial
import PySimpleGUI as sg


uart = serial.Serial()


def settings_tab():
    settings_com_ports = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7',
                          'COM8', 'COM9', 'COM10', 'COM11', 'COM12', 'COM13', 'COM14',
                          'COM15', 'COM16', 'COM17', 'COM18', 'COM19']

    settings_baudrate = ['9600', '14400', '19200', '38400', '57600', '115200']

    settings_output = sg.Multiline(key='settings window', size=(100, 4))

    settings_layout = [[sg.Text('COM ports'), sg.Text('Baud rate')],
                       [sg.Listbox(settings_com_ports, default_values=['COM1'], size=(7, 5), enable_events=True),
                        sg.Listbox(settings_baudrate, default_values=['9600'], size=(7, 5), enable_events=True)],
                       [sg.Button('Open port'), sg.Button('Close port')],
                       [settings_output]]

    settings_window = sg.Window('Settings', settings_layout)

    while True:

        settings_event, settings_values = settings_window.read()

        if settings_event in (sg.WIN_CLOSED, 'Exit'):
            break

        else:

            com_port = ''.join(settings_values[0])  # convert tuple into string
            baud = ''.join(settings_values[1])  # convert tuple into string

            if settings_event == 'Open port':

                if uart.isOpen():  # if port is already opened, do not try to open it once again

                    if uart.port == com_port:  # when selected setting covers port which is already opened

                        settings_window['settings window'].update('')
                        settings_output.print("The port is already opened")

                    else:  # when other port is already opened, and someone is trying to open another one

                        settings_window['settings window'].update('')  # clear window
                        settings_output.print(uart.port, "is already opened, do not try to open another port")

                else:  # the port is not under usage, it can be opened

                    uart.port = com_port
                    uart.baudrate = int(baud)  # convert string into number

                    try:  # the code which may raise exception SerialException
                        uart.open()

                    except serial.SerialException:  # if SerialException will occur, do the management action

                        settings_window['settings window'].update('')  # clear window
                        settings_output.print("Something went wrong... \n The port cannot be opened")

                    else:  # otherwise, inform that everything went along nicely

                        settings_window['settings window'].update('')  # clear window
                        settings_output.print("The port has been successfully opened")

            if settings_event == 'Close port':

                if uart.isOpen():

                    uart.close()
                    settings_window['settings window'].update('')
                    settings_output.print(uart.port, " has just been closed")

                else:

                    settings_window['settings window'].update('')
                    settings_output.print("It's difficult to close port which is not even opened ... :(")

    settings_window.close()
    del settings_window  # destructor, deletes setting_window object