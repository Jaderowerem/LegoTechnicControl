import PySimpleGUI
import time
import os.path

from Settings import *  # include all namespace from Settings.py file
from Tools import *  # from Tools import everything
from Help import *  # from Help import everything
from MySimpleProtocol_ZigBee import *  # from Zigbee import everything
import PySimpleGUI as sg

myProjectVersion = "0.2.30"
file_serial_read_path = ""


def runApp():
    """
    RunApp is the main process of the GUI application, here other components
    will be added
    """

    global file_serial_read_path  # the global variable is going to be edited inside the module

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
    app_main_menu = sg.Menu(menu_def, tearoff=False, pad=(200, 1), key='-MAIN_MENU-')
    app_window_receive_text = sg.Text("Receive window", pad=(0, 5))
    app_window_receive = sg.Multiline(key='-RECEIVE-', size=(50, 6))
    app_window_transmit_text = sg.Text("Send window", pad=(0, 5))
    app_window_transmit = sg.Input(key='-TRANSMIT-', size=(50, 1), pad=(0, 0))

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
    app_serial_port_tab_send_message = sg.Button("SEND", size=(12, 1), pad=((40, 0), (0, 0)), key="SEND")
    # key defines name of events and values (key of dictionary)
    app_serial_port_tab_read = sg.Button("READ", size=(12, 1), pad=((20, 0), (90, 0)), key="READ")
    app_serial_port_tab_devices_text = sg.Text(" Device ", pad=((505, 0), (0, 0)))

    app_serial_port_devices = ["Device A", "Device B"]

    app_serial_port_tab_devices = sg.Listbox(app_serial_port_devices, default_values=["Device A"], size=(9, 3),
                                             enable_events=True, key="DEVICE ON PORT", pad=((20, 10), (0, 55)))

    zigbee_serial_ports = ['COM0', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7',
                           'COM8', 'COM9', 'COM10', 'COM11', 'COM12', 'COM13', 'COM14',
                           'COM15', 'COM16', 'COM17', 'COM18', 'COM19']

    zigbee_baudrate = ['9600', '14400', '19200', '38400', '57600', '115200']

    zigbee_signal_channel = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
                             '22', '23', '24', '25', '26']

    app_zigbee_tab_serial_channel = sg.Listbox(zigbee_serial_ports, default_values=['COM0'], size=(7, 5),
                                               enable_events=True, key="ZIGBEE_SETTING_PORT", pad=((10, 40), (0, 0)))

    app_zigbee_tab_serial_baudrate = sg.Listbox(zigbee_baudrate, default_values=['9600'], size=(7, 5),
                                                enable_events=True, key="ZIGBEE_SETTING_BAUDRATE",
                                                pad=((0, 40), (0, 0)))

    app_zigbee_tab_signal_channel = sg.Listbox(zigbee_signal_channel, default_values=['11'], size=(7, 5),
                                               enable_events=True, key="ZIGBEE_SETTING_CHANNEL", pad=((0, 40), (0, 0)))

    app_zigbee_tab_panid_input = sg.Input(key='ZIGBEE_SET_PANID', size=(10, 1), pad=((0, 10), (0, 80)))
    app_zigbee_tab_addrA_input = sg.Input(key='ZIGBEE_ADDR_A', size=(10, 1), pad=((0, 100), (10, 0)))
    app_zigbee_tab_addrB_input = sg.Input(key='ZIGBEE_ADDR_B', size=(10, 1), pad=((0, 0), (10, 0)))

    app_zigbee_button_menu_commands = ["UNUSED", ["RESTART MODULE", "SET FACTORY SETTINGS", "SET SERIAL PORT",
                                                  "SET SIGNAL CHANNEL", "SET PANID", "GET CONFIGURATION",
                                                  "GET SERIAL PORT", "GET SIGNAL CHANNEL", "GET PANID",
                                                  "GET SHORT ADDRESS OF THE DEVICE", "GET SHORT PARENT ADDRESS",
                                                  "GET DEVICE IEEE ADDRESS", "GET PARENT IEEE ADDRESS",
                                                  "PACKET FROM MODULE A TO B", "PACKET FROM MODULE B TO A"]]

    app_zigbee_tab_commands = sg.ButtonMenu("ZigBee command", menu_def=app_zigbee_button_menu_commands,
                                            pad=((10, 230), (10, 0)), key="ZIGBEE_COMMAND")

    app_zigbee_tab_serial_channel_text = sg.Text(" Serial channel", pad=(0, 10))
    app_zigbee_tab_serial_baudrate_text = sg.Text("Baud rate", pad=(20, 10))
    app_zigbee_tab_signal_channel_text = sg.Text("Signal channel", pad=((20, 0), (0, 0)))
    app_zigbee_tab_signal_panid_text = sg.Text("PANID", pad=((50, 0), (0, 0)))
    app_zigbee_tab_signal_panid_info = sg.Text("Set address 0000 - 3FFE", pad=((0, 0), (0, 80)))
    # pad: ((distance from left corner of element, distance from right corner), (go down, go up))
    app_zigbee_tab_commands_text = sg.Text("Commands", pad=((10, 225), (30, 0)))
    app_zigbee_tab_addrA_text = sg.Text("Address of module A", pad=((0, 50), (30, 0)))
    app_zigbee_tab_addrB_text = sg.Text("Address of module B", pad=((0, 0), (30, 0)))

    app_msp_tab_obj_names_text = sg.Text("Object name - label value", pad=((10, 0), (10, 0)))
    app_msp_tab_obj_adding_object_text = sg.Text("Object-label value", pad=((10, 0), (10, 0)))
    app_msp_tab_obj_value_text = sg.Text("Insert object value", pad=((10, 0), (10, 0)))

    app_msp_tab_obj_names_label_val = []

    app_msp_tab_adding_obj_input = sg.Input(key='Adding new object', size=(30, 1), pad=((10, 10), (0, 0)))
    app_msp_tab_value_obj_input = sg.Input(key='Inserting obj value', size=(14, 1), pad=((10, 0), (0, 0)))
    app_msp_tab_listbox = sg.Listbox(app_msp_tab_obj_names_label_val, default_values=[""], size=(25, 5),
                                     enable_events=True, key="OBJ NAMES", pad=((10, 10), (0, 10)))

    app_msp_tab_add_obj_button = sg.Button("ADD OBJECT", pad=((10, 10), (10, 10)))
    app_msp_tab_rm_obj_button = sg.Button("REMOVE OBJECT", pad=((0, 0), (10, 10)))
    app_msp_tab_send_msp_button = sg.Button("SEND (MSP)", pad=((20, 0), (0, 5)))

    app_msp_tab_trans_status = sg.Text("No transmission started yet", size=(25, 1), pad=((10, 0), (0, 0)))

    app_msp_frame1 = sg.Frame("Objects", layout=[[app_msp_tab_obj_names_text],
                                                 [app_msp_tab_listbox]],
                              pad=((10, 10), (10, 0)))

    app_msp_frame2 = sg.Frame("Add new object",
                              layout=[[app_msp_tab_obj_adding_object_text], [app_msp_tab_adding_obj_input],
                                      [app_msp_tab_add_obj_button,
                                       app_msp_tab_rm_obj_button]], pad=((0, 0), (0, 30)))

    app_msp_frame3 = sg.Frame("MySimpleProtocol (MSP)", layout=[[app_msp_tab_obj_value_text],
                                                                [app_msp_tab_value_obj_input,
                                                                 app_msp_tab_send_msp_button,
                                                                 app_msp_tab_trans_status]], pad=((10, 10), (10, 10)))

    """
    2.
    """
    app_serial_port_tab_layout = [[app_serial_port_tab_file_section],
                                  [app_serial_port_tab_file_to_send, app_serial_port_tab_file_to_record,
                                   app_serial_port_tab_send_file, app_serial_port_tab_read_to_file,
                                   app_serial_port_tab_close_file],
                                  ]

    app_zigbee_tab_layout = [[app_zigbee_tab_serial_channel_text, app_zigbee_tab_serial_baudrate_text,
                              app_zigbee_tab_signal_channel_text,
                              app_zigbee_tab_signal_panid_text],
                             [app_zigbee_tab_serial_channel, app_zigbee_tab_serial_baudrate,
                              app_zigbee_tab_signal_channel, app_zigbee_tab_panid_input,
                              app_zigbee_tab_signal_panid_info], [app_zigbee_tab_commands_text,
                                                                  app_zigbee_tab_addrA_text, app_zigbee_tab_addrB_text],
                             [app_zigbee_tab_commands, app_zigbee_tab_addrA_input, app_zigbee_tab_addrB_input]]

    app_msp_tab_layout = [[app_msp_frame1, app_msp_frame2],
                          [app_msp_frame3]]
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
        [app_window_receive_text, app_serial_port_tab_devices_text],
        [app_window_receive, app_serial_port_tab_read, app_serial_port_tab_devices],
        [app_window_transmit_text],
        [app_window_transmit, app_serial_port_tab_send_message],
        [app_tab_group]
    ]
    """
    Create main window object
    """
    app_window = sg.Window('LEGO Technic PC control',
                           app_main_layout,
                           default_element_size=(15, 1),
                           default_button_element_size=(12, 1), size=(800, 700))

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

        elif event == "ADD OBJECT":

            obj = app_msp_tab_adding_obj_input.get()
            inx = obj.find("-")
            obj_name = obj[0:inx]
            new_key = obj[(inx + 1)::]

            """
            Add a new object to the data base
            """
            app_msp_tab_obj_names_label_val.append(obj)
            app_msp_tab_listbox.update(app_msp_tab_obj_names_label_val)
            MSP_Obj_database[new_key] = obj_name  # for dictionary, there is no append(), add() , etc function,
            # this is the way to add new elements to dictionary

        elif event == "REMOVE OBJECT":
            pass

        elif event == "SEND (MSP)":

            try:
                MySimpleProtocol_transmit("10 100", "CTRL", "8DF3", "0000", device)  # test

            except MySimpleProtocolDataLength:
                app_msp_tab_trans_status.update("Packet length problem", text_color="red")  # update transmission status

            except MySimpleProtocolCRC8:
                app_msp_tab_trans_status.update("Incorrect CRC-8 received", text_color="red")

            except MySimpleProtocolStatus:
                app_msp_tab_trans_status.update("NOK or unsupported status received", text_color="red")

            else:
                app_msp_tab_trans_status.update("OK", text_color="green")

    app_window.close()
    del app_window


runApp()

if uart["Device A"].isOpen():
    uart["Device A"].close()  # when main program was finished and port was not closed, close it
    del uart["Device A"]

if uart["Device B"].isOpen():
    uart["Device B"].close()  # when main program was finished and port was not closed, close it
    del uart["Device B"]
