import time
import os.path

from Settings import *  # include all namespace from Settings.py file
from Tools import *  # from Tools import everything
from Help import *  # from Help import everything
from MySimpleProtocol_ZigBee import *  # from Zigbee import everything
import PySimpleGUI as sg

myProjectVersion = "0.3.10"


def runApp():
    """
    RunApp is the main process of the GUI application, here other components
    will be added
    """

    Calculate_CRC8_lookUpTable(CRC8_lookuptable, 0xA7, "decimal")  # fill up CRC-8 look up table

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

    """
    Main UI 
    """
    app_main_menu = sg.Menu(menu_def, tearoff=False, pad=(200, 1), key='-MAIN_MENU-')
    app_window_receive = sg.Multiline(key='-RECEIVE-', size=(50, 6), pad=((10, 10), (10, 10)))
    app_window_transmit = sg.Input(key='-TRANSMIT-', size=(50, 1), pad=((10, 10), (10, 10)))

    app_window_frame1 = sg.Frame("Receive window", layout=[[app_window_receive]],
                                 pad=((10, 10), (10, 10)),
                                 element_justification="center",
                                 vertical_alignment="center"
                                 )

    app_window_frame2 = sg.Frame("Send window", layout=[[app_window_transmit]],
                                 pad=((10, 10), (0, 10)),
                                 element_justification="center",
                                 vertical_alignment="center"
                                 )

    app_window_frame = sg.Frame("Transmission", layout=[[app_window_frame1],
                                                        [app_window_frame2]],
                                pad=((10, 10), (10, 10)),
                                element_justification="center",
                                vertical_alignment="center"
                                )
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
    """
    App pictures
    """
    app_picture1 = sg.Image(filename="picture1.PNG")
    """
    Serial port UI 
    """
    app_serial_port_tab_file_section = sg.Text(" File ", pad=(0, 10))
    app_serial_port_tab_file_to_send = sg.Button("FILE TO SEND", size=(14, 1), pad=(10, 10))
    app_serial_port_tab_send_file = sg.Button("SEND FILE", size=(12, 1), pad=(10, 0))
    app_serial_port_tab_file_to_record = sg.Button("FILE TO RECORD DATA", size=(22, 1), pad=(0, 0))
    app_serial_port_tab_read_to_file = sg.Button("READ TO FILE", size=(14, 1), pad=(0, 0))
    app_serial_port_tab_close_file = sg.Button("CLOSE FILE", size=(15, 1), pad=(10, 0))
    app_serial_port_tab_send_button = sg.Button("SEND", size=(12, 1), pad=((10, 10), (10, 10)), key="SEND")
    # key defines name of events and values (key of dictionary)
    app_serial_port_tab_read_button = sg.Button("READ", size=(12, 1), pad=((10, 10), (10, 10)), key="READ")

    app_serial_port_devices = ["Device A", "Device B"]

    app_serial_port_tab_devices_list = sg.Listbox(app_serial_port_devices, default_values=["Device A"], size=(9, 3),
                                                  enable_events=True, key="DEVICE ON PORT", pad=((10, 10), (10, 10)))

    app_serial_port_devices_frame = sg.Frame("Device", layout=[[app_serial_port_tab_devices_list]],
                                             pad=((10, 10), (10, 10)),
                                             element_justification="center",
                                             vertical_alignment="center")

    app_serial_port_buttons_frame = sg.Frame("", layout=[[app_serial_port_tab_send_button],
                                                         [app_serial_port_tab_read_button]
                                                         ],
                                             pad=((10, 10), (10, 10)),
                                             element_justification="center",
                                             vertical_alignment="center")

    app_serial_port_buttons_devices_frame = sg.Frame("", layout=[[app_serial_port_devices_frame],
                                                                 [app_serial_port_buttons_frame],
                                                                 ],
                                                     pad=((10, 10), (10, 10)),
                                                     element_justification="center",
                                                     vertical_alignment="center")
    """
    ZigBee UI 
    """
    zigbee_serial_ports = ['COM0', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7',
                           'COM8', 'COM9', 'COM10', 'COM11', 'COM12', 'COM13', 'COM14',
                           'COM15', 'COM16', 'COM17', 'COM18', 'COM19']

    zigbee_baudrate = ['9600', '14400', '19200', '38400', '57600', '115200']

    zigbee_signal_channel = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
                             '22', '23', '24', '25', '26']

    app_zigbee_tab_serial_port_list = sg.Listbox(zigbee_serial_ports, default_values=['COM0'], size=(7, 5),
                                                 enable_events=True, key="ZIGBEE_SETTING_PORT",
                                                 pad=((10, 10), (10, 10)))

    app_zigbee_tab_serial_baudrate_list = sg.Listbox(zigbee_baudrate, default_values=['9600'], size=(7, 5),
                                                     enable_events=True, key="ZIGBEE_SETTING_BAUDRATE",
                                                     pad=((10, 10), (10, 10)))

    app_zigbee_tab_signal_channel_list = sg.Listbox(zigbee_signal_channel, default_values=['11'], size=(7, 5),
                                                    enable_events=True, key="ZIGBEE_SETTING_CHANNEL",
                                                    pad=((10, 10), (10, 10)))

    app_zigbee_tab_panid_input = sg.Input(key='ZIGBEE_SET_PANID', size=(10, 1), pad=((10, 10), (10, 10)))
    app_zigbee_tab_addrA_input = sg.Input(key='ZIGBEE_ADDR_A', size=(10, 1), pad=((10, 10), (10, 10)))
    app_zigbee_tab_addrB_input = sg.Input(key='ZIGBEE_ADDR_B', size=(10, 1), pad=((10, 10), (10, 10)))

    app_zigbee_tab_menubutton_commands_set = ["UNUSED", ["RESTART MODULE", "SET FACTORY SETTINGS", "SET SERIAL PORT",
                                                         "SET SIGNAL CHANNEL", "SET PANID", "GET CONFIGURATION",
                                                         "GET SERIAL PORT", "GET SIGNAL CHANNEL", "GET PANID",
                                                         "GET SHORT ADDRESS OF THE DEVICE", "GET SHORT PARENT ADDRESS",
                                                         "GET DEVICE IEEE ADDRESS", "GET PARENT IEEE ADDRESS",
                                                         "PACKET FROM MODULE A TO B", "PACKET FROM MODULE B TO A"]]

    app_zigbee_tab_menubutton_commands = sg.ButtonMenu("ZigBee commands",
                                                       menu_def=app_zigbee_tab_menubutton_commands_set,
                                                       pad=((10, 10), (10, 10)), key="ZIGBEE_COMMAND")

    app_zigbee_tab_panid_text = sg.Text("Set address 0000 - 3FFE", pad=((0, 10), (10, 10)))
    # pad: ((distance from left corner of element, distance from right corner), (distance from floor, dist. from top))

    app_zigbee_conf_frame1 = sg.Frame("Baud rate", layout=[[app_zigbee_tab_serial_baudrate_list]],
                                      pad=((10, 10), (10, 10)))
    app_zigbee_conf_frame2 = sg.Frame(" Serial port", layout=[[app_zigbee_tab_serial_port_list]],
                                      pad=((10, 10), (10, 10)))
    app_zigbee_conf_frame3 = sg.Frame("RF channel", layout=[[app_zigbee_tab_signal_channel_list]],
                                      pad=((10, 10), (10, 10)))
    app_zigbee_conf_frame4 = sg.Frame("PANID", layout=[[app_zigbee_tab_panid_input,
                                                        app_zigbee_tab_panid_text]],
                                      pad=((10, 10), (10, 10)))

    app_zigbee_conf_frame = sg.Frame("ZigBee module settings", layout=[[app_zigbee_conf_frame1,
                                                                        app_zigbee_conf_frame2,
                                                                        app_zigbee_conf_frame3,
                                                                        app_zigbee_conf_frame4]],
                                     pad=((10, 10), (10, 10)))

    app_zigbee_addr_frame1 = sg.Frame("Address of module A", layout=[[app_zigbee_tab_addrA_input]],
                                      pad=((10, 10), (10, 10)))

    app_zigbee_addr_frame2 = sg.Frame("Address of module B", layout=[[app_zigbee_tab_addrB_input]],
                                      pad=((10, 10), (10, 10)))

    app_zigbee_addr_frame = sg.Frame("ZigBee addresses", layout=[[app_zigbee_addr_frame1,
                                                                  app_zigbee_addr_frame2]],
                                     pad=((10, 10), (10, 10)))

    app_zigbee_commands_frame = sg.Frame("ZigBee commands", layout=[[app_zigbee_tab_menubutton_commands]],
                                         pad=((10, 10), (10, 10)))
    """
    MSP UI
    """
    app_msp_tab_obj_names_text = sg.Text("Object name", pad=((10, 0), (10, 0)))
    app_msp_tab_obj_value_text = sg.Text("Insert object value", pad=((10, 0), (10, 0)))

    app_msp_tab_obj_names_label_val = ['test1Obj', 'test2Obj']  # the reflection of MSP_Obj_database keys

    app_msp_tab_simple_input = sg.Input(key='Simple_obj_value', size=(14, 1), pad=((10, 0), (0, 0)))

    app_msp_tab_multi_start = sg.Input(key='Multi_start_obj_value', size=(14, 1), pad=((10, 10), (10, 10)))
    app_msp_tab_multi_stop = sg.Input(key='Multi_stop_obj_value', size=(14, 1), pad=((10, 10), (10, 10)))
    app_msp_tab_multi_step = sg.Input(key='Multi_step_obj_value', size=(14, 1), pad=((10, 10), (10, 10)))
    app_msp_tab_multi_loop = sg.Input(key='Multi_loop', size=(6, 1), pad=((10, 10), (10, 10)))
    app_msp_tab_multi_dwellTime = sg.Input(key='Multi_dwellTime', size=(6, 1), pad=((10, 10), (10, 10)))

    app_msp_tab_listbox = sg.Listbox(app_msp_tab_obj_names_label_val, default_values=["test1Obj"], size=(25, 5),
                                     enable_events=True, key="Obj_Name", pad=((10, 10), (0, 10)))

    app_msp_tab_send_msp_simple_button = sg.Button("SEND (SIMPLE)", pad=((10, 0), (10, 10)))
    app_msp_tab_send_msp_multi_button = sg.Button("SEND (MULTI)", pad=((10, 0), (10, 10)))
    app_msp_tab_interrupt_msp_multi_button = sg.Button("INTERRUPT (MULTI)", pad=((10, 0), (10, 10)))

    app_msp_tab_trans_simple_status = sg.Text("Simple transfer status", size=(15, 3),
                                              justification="center",
                                              pad=((10, 10), (10, 0)),
                                              key="Simple_status")

    app_msp_tab_trans_multi_status = sg.Text("Multiple transfer status", size=(15, 3),
                                             justification="center",
                                             pad=((10, 10), (10, 0)),
                                             key="Multi_status")

    app_msp_tab_trans_multi_currentValue = sg.Text("Current object value", size=(15, 1),
                                                   justification="center",
                                                   pad=((10, 10), (10, 0)),
                                                   key="Multi_current_val")

    app_msp_frame1 = sg.Frame("Objects", layout=[[app_msp_tab_obj_names_text],
                                                 [app_msp_tab_listbox]],
                              pad=((10, 10), (10, 0)),
                              vertical_alignment="top")

    app_msp_simple_frame = sg.Frame("Simple transfer", layout=[[app_msp_tab_obj_value_text],
                                                               [app_msp_tab_simple_input,
                                                                app_msp_tab_send_msp_simple_button,
                                                                app_msp_tab_trans_simple_status]],
                                    pad=((10, 10), (10, 10)),
                                    vertical_alignment="top")

    app_msp_multi_start_frame = sg.Frame("Start value", layout=[[app_msp_tab_multi_start]],
                                         pad=((10, 10), (10, 10)),
                                         vertical_alignment="top")

    app_msp_multi_stop_frame = sg.Frame("Stop value", layout=[[app_msp_tab_multi_stop]],
                                        pad=((10, 10), (10, 10)),
                                        vertical_alignment="top")

    app_msp_multi_step_frame = sg.Frame("Step", layout=[[app_msp_tab_multi_step]],
                                        pad=((10, 10), (10, 10)),
                                        vertical_alignment="top")

    app_msp_multi_loop_frame = sg.Frame("Loop count", layout=[[app_msp_tab_multi_loop]],
                                        pad=((10, 10), (10, 10)),
                                        vertical_alignment="top")

    app_msp_multi_dwellTime_frame = sg.Frame("Dwell time [sec]", layout=[[app_msp_tab_multi_dwellTime]],
                                             pad=((10, 10), (10, 10)),
                                             vertical_alignment="top")

    app_msp_multi_frame = sg.Frame("Multiple transfer", layout=[[app_msp_multi_start_frame, app_msp_multi_stop_frame,
                                                                 app_msp_multi_step_frame],
                                                                [app_msp_multi_loop_frame,
                                                                 app_msp_multi_dwellTime_frame,
                                                                 app_msp_tab_send_msp_multi_button,
                                                                 app_msp_tab_interrupt_msp_multi_button,
                                                                 app_msp_tab_trans_multi_status],
                                                                [app_msp_tab_trans_multi_currentValue]
                                                                ],
                                   pad=((10, 10), (10, 10)),
                                   vertical_alignment="top")

    app_msp_main_frame = sg.Frame("MySimpleProtocol (MSP)", layout=[[app_msp_simple_frame], [app_msp_multi_frame]],
                                  pad=((10, 10), (10, 10)),
                                  vertical_alignment="top")
    """
    2.
    """
    app_serial_port_tab_layout = [[app_serial_port_tab_file_section],
                                  [app_serial_port_tab_file_to_send, app_serial_port_tab_file_to_record,
                                   app_serial_port_tab_send_file, app_serial_port_tab_read_to_file,
                                   app_serial_port_tab_close_file],
                                  ]

    app_zigbee_tab_layout = [[app_zigbee_conf_frame],
                             [app_zigbee_addr_frame, app_zigbee_commands_frame]]

    app_msp_tab_layout = [[app_msp_frame1, app_msp_main_frame]]

    """
    3.
    """
    app_serial_port_tab = sg.Tab(" Serial port ", layout=app_serial_port_tab_layout, key="-SERIAL_PORT-")

    app_zigbee_tab = sg.Tab(" Zigbee ", layout=app_zigbee_tab_layout, key="-ZIGBEE_TAB-", pad=(0, 20))

    app_msp_tab = sg.Tab(" My Simple Protocol ", layout=app_msp_tab_layout, key="-MSP-")

    """
    4.
    """
    layout_tabs = [  # layout of group of tabs
        [app_serial_port_tab],
        [app_zigbee_tab],
        [app_msp_tab]
    ]

    app_tab_group = sg.TabGroup(layout_tabs)  # create tab group object which includes all tabs

    app_main_layout = [
        [app_main_menu],
        [app_window_frame, app_serial_port_buttons_devices_frame, app_picture1],
        [app_tab_group]
    ]
    """
    Create main window object
    """
    app_window = sg.Window('LEGO Technic PC control',
                           app_main_layout,
                           default_element_size=(10, 1),
                           default_button_element_size=(12, 1), size=(1200, 900))

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

        device = ''.join(values["DEVICE ON PORT"])  # converts tuple or list into string, get proper device- A or B

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

            if txd_data == zigbee_commands_set["GET SHORT ADDRESS OF THE DEVICE"]:

                serial_port_send_command(uart[device], txd_data)
                time.sleep(0.1)

                if device == "Device A":

                    str_b = str(uart[device].read(11), "UTF-8")
                    show_device_addr(str_b, app_zigbee_tab_addrA_input)
                    uart[device].reset_input_buffer()  # clear input buffer after data has just been read

                elif device == "Device B":

                    str_b = str(uart[device].read(11), "UTF-8")
                    show_device_addr(str_b, app_zigbee_tab_addrB_input)
                    uart[device].reset_input_buffer()  # clear input buffer after data has just been read

            else:

                serial_port_send_command(uart[device], txd_data)

        elif event == "FILE TO RECORD DATA":

            file_serial_read_path = sg.popup_get_file('File to open', no_window=True)  # returns path to the file
            # print(file_serial_read_path)

            try:

                file_serial_read = open(file_serial_read_path, 'wb')

            except OSError:

                app_window_receive.print("The file cannot be opened")

        elif event == "READ TO FILE":

            if os.path.isfile(file_serial_read_path):  # first check if the file exists

                serial_port_read_to_file(uart[device], file_serial_read, 100)
            else:

                app_window["-RECEIVE-"].update("The file does not exist !!!")

        elif event == "READ":

            serial_port_read_to_window(uart[device], app_window_receive, 100)  # it reads up to 100 bytes or less but
            # within timeout, when timeout is exceeded, it breaks the readout,
            # so two factors must be tuned: timeout and number of bytes to read

            pass

        elif event == "CLOSE FILE":

            if os.path.isfile(file_serial_read_path):  # first check if the file exists

                file_serial_read.close()

        elif event == "ZIGBEE_COMMAND":

            get_zigbee_command(values, app_window_transmit)

        elif event == "SEND (SIMPLE)":
            #   print(MSP_Obj_database[ObjName] + " " + ObjVal)

            if uart[device].isOpen():

                ObjVal = app_msp_tab_simple_input.get()
                ObjName = ''.join(values["Obj_Name"])  # converts tuple or list or dictionary into string

                try:
                    MySimpleProtocol_transmit(MSP_Obj_database[ObjName] + " " + ObjVal, "CTRL", "8DF3",
                                              "0000", device)  # test

                except MySimpleProtocolDataLength:

                    app_window = app_window.finalize()  # according to PySimpleGui documentation
                    app_window["Simple_status"].update("Packet length problem", text_color="red")
                    break

                except MySimpleProtocolCRC8:

                    app_window = app_window.finalize()  # according to PySimpleGui documentation
                    app_window["Simple_status"].update("Incorrect CRC-8 received", text_color="red")
                    break

                except MySimpleProtocolStatusNok:

                    app_window = app_window.finalize()  # according to PySimpleGui documentation
                    app_window["Simple_status"].update("NOK status received", text_color="red")
                    break

                except MySimpleProtocolStatusUnsupported:

                    app_window = app_window.finalize()  # according to PySimpleGui documentation
                    app_window["Simple_status"].update("Unsupported status received", text_color="red")
                    break

                else:
                    app_window = app_window.finalize()  # according to PySimpleGui documentation
                    app_window["Simple_status"].update("OK", text_color="green")

            else:
                app_window = app_window.finalize()  # according to PySimpleGui documentation
                app_window["Simple_status"].update("Serial port is not opened !", text_color="yellow")

        elif event == "SEND (MULTI)":

            if uart[device].isOpen():

                loopCount = int(app_msp_tab_multi_loop.get())
                dwellTime = float(app_msp_tab_multi_dwellTime.get())
                startVal = int(app_msp_tab_multi_start.get())
                stopVal = int(app_msp_tab_multi_stop.get())
                stepVal = int(app_msp_tab_multi_step.get())

                #   print("loopCount: ", loopCount)
                #   print("dwellTime: ", dwellTime)
                #   print("startVal: ", startVal)
                #   print("stopVal: ", stopVal)
                #   print("stepVal : ", stepVal)

                ObjName = ''.join(values["Obj_Name"])  # converts tuple or list or dictionary into string

                """for "for" loop, iteration element is being incremented from start until stop value but without 
                reaching stop value, [start value, stop value) -> one-sided open set,
                in this case to reach stop value too -> stopVal = stopVal + stepVal
                """
                stopVal = stopVal + stepVal
                interruptTransfer = 0

                while loopCount > 0 and interruptTransfer != 1:

                    loopCount -= 1

                    for val in range(startVal, stopVal, stepVal):

                        """
                        check if interruption of multiple transfer occurred or it can be continued
                        """

                        inter_event, inter_val = app_window.read(timeout=1)

                        if inter_event == "INTERRUPT (MULTI)":
                            interruptTransfer = 1
                            app_window = app_window.finalize()  # according to PySimpleGui documentation
                            app_window["Multi_status"].update("Multiple transfer interrupted on request",
                                                              text_color="yellow")
                            break   # exit for loop

                        else:
                            val_str = str(val)
                            print(MSP_Obj_database[ObjName] + " " + val_str)

                            app_window = app_window.finalize()  # according to PySimpleGui documentation
                            app_window["Multi_current_val"].update(val_str)

                            try:
                                MySimpleProtocol_transmit(MSP_Obj_database[ObjName] + " " + val_str, "CTRL", "8DF3",
                                                          "0000", device)  # test

                            except MySimpleProtocolDataLength:

                                app_window = app_window.finalize()  # according to PySimpleGui documentation
                                app_window["Multi_status"].update("Packet length problem", text_color="red")
                                interruptTransfer = 1
                                break

                            except MySimpleProtocolCRC8:

                                app_window = app_window.finalize()  # according to PySimpleGui documentation
                                app_window["Multi_status"].update("Incorrect CRC-8 received", text_color="red")
                                interruptTransfer = 1
                                break

                            except MySimpleProtocolStatusNok:

                                app_window = app_window.finalize()  # according to PySimpleGui documentation
                                app_window["Multi_status"].update("NOK status received", text_color="red")
                                interruptTransfer = 1
                                break

                            except MySimpleProtocolStatusUnsupported:

                                app_window = app_window.finalize()  # according to PySimpleGui documentation
                                app_window["Multi_status"].update("Unsupported status received", text_color="red")
                                interruptTransfer = 1
                                break

                            else:
                                app_window = app_window.finalize()  # according to PySimpleGui documentation
                                app_window["Multi_status"].update("OK", text_color="green")

                        time.sleep(dwellTime)  # delay period

            else:
                app_window = app_window.finalize()  # according to PySimpleGui documentation
                app_window["Multi_status"].update("Serial port is not opened !", text_color="yellow")

            print("end of while loop")

    app_window.close()
    del app_window


runApp()

if uart["Device A"].isOpen():
    uart["Device A"].close()  # when main program was finished and port was not closed, close it
    del uart["Device A"]

if uart["Device B"].isOpen():
    uart["Device B"].close()  # when main program was finished and port was not closed, close it
    del uart["Device B"]
