import subprocess
import pyvisa
import time
import sys
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import numpy as np
import pandas as pd
import serial

visa_SA = 'TCPIP0::192.168.0.13::inst0::INSTR'
rm = pyvisa.ResourceManager()
time.sleep(2)
SA = rm.open_resource(visa_SA)

set_frequency = 16000
set_pwr = 10

list_of_values=[]
values={}

serial_port = 'COM5'
serial_baudrate = 115200
u25_cmd = 'dsa_u25\n'
u26_cmd = 'dsa_u26\n'
u27_cmd = 'dsa_u27\n'

u25_range=[]
u26_range=[]
u27_range=[]

def serial_module_config(port='COM5', baudrate=115200, timeout=5):
    try:
        # Open the serial port
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            # Give some time for the serial connection to establish
            time.sleep(2)
            
            # Flush any existing input/output
            ser.flushInput()
            ser.flushOutput()
            
            # Send the command to the device
            ser.write(("8V_RF_ON\n"+ '\r').encode())
            ser.write(("5V_RF_ON\n"+ '\r').encode())
            ser.write(("3V_RF_ON\n"+ '\r').encode())
            ser.write(("tune_maap\n"+ '\r').encode())
            ser.write(("set_point 37\n"+ '\r').encode())
            ser.write(("thermal_control on\n"+ '\r').encode())
            ser.write(("gen_rf 16000 10\n"+ '\r').encode())
            
            # Wait for a response
            time.sleep(1)
            
            # Read the response
            response = ser.read_all().decode().strip()
            
            return response
    except serial.SerialException as e:
        return f"Serial error: {e}"
    except Exception as e:
        return f"Error: {e}"
    


def serial_command(port, baudrate, command, timeout=5):
    try:
        # Open the serial port
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            # Give some time for the serial connection to establish
            time.sleep(2)
            
            # Flush any existing input/output
            ser.flushInput()
            ser.flushOutput()
            
            # Send the command to the device
            ser.write((command + '\r').encode())
            
            
            # Wait for a response
            time.sleep(1)
            
            # Read the response
            response = ser.read_all().decode().strip()
            
            return response
    except serial.SerialException as e:
        return f"Serial error: {e}"
    except Exception as e:
        return f"Error: {e}"



def open_teraterm():
    # path = r'C:\Program Files (x86)\teraterm\ttermpro.exe'
    path = r"C:\Program Files (x86)\teraterm\ttermpro.exe"
    comport = 5
    Baudrate = 115200
    process=subprocess.Popen(f'{path} /C={comport} /BAUD={Baudrate}', stdout=subprocess.PIPE, text=True)
    time.sleep(2)

def DSA():
    try:
        print('Connecting to Spectrum Analyzer...')
        SA = rm.open_resource(visa_SA)
        SA.timeout = 5000

    except:
        print('Cannot connect to Spectrum Analyzer. Exiting now...')
        sys.exit()

    else:
        print('Spectrum Analyzer connected')

    try:
        TT = Application().connect(title="COM5 - Tera Term VT")  
        terminal = TT.window(title="COM5 - Tera Term VT")
        my_range = [4,3.5,3,2.5,2,1.5,1,0]
        terminal.type_keys(f"gen_rf 16000 10", with_spaces=True)

        # get the current DSAs values after genrf command
        terminal.type_keys(f"dsa_u25", with_spaces=True)
        terminal.type_keys("{ENTER}")  
        # read the value and store it in the variable and make a different range for each element
        
        terminal.type_keys(f"dsa_u26", with_spaces=True)
        terminal.type_keys("{ENTER}")  
        # read the value and store it in the variable and make a different range for each element

        terminal.type_keys(f"dsa_u27", with_spaces=True)
        terminal.type_keys("{ENTER}")
        # read the value and store it in the variable and make a different range for each element

    
        for dsa_U27 in my_range:
            for dsa_u26 in my_range:
                for dsa_u25 in my_range:
                    #print(str(dsa_u25) + ',' + str(dsa_u26) + ',' + str(dsa_U27))
                    terminal.type_keys(u"dac_maam 0", with_spaces=True)
                    terminal.type_keys("{ENTER}")
                    terminal.type_keys(f"dsa_u25 {dsa_u25}", with_spaces=True)
                    terminal.type_keys("{ENTER}")  
                    terminal.type_keys(f"dsa_u26 {dsa_u26}", with_spaces=True)
                    terminal.type_keys("{ENTER}")  
                    terminal.type_keys(f"dsa_u27 {dsa_U27}", with_spaces=True)
                    terminal.type_keys("{ENTER}")

                    time.sleep(2)

                    values['frequency'] = str(set_frequency)
                    values['set_pwr'] = str(set_pwr)
                    values['DSA_U25'] = 4


                    SA.write(f'FREQ:CENT 16000 MHZ')        
                    SA.write('*TRG;*WAI')   
                    SA.write(":FREQ:TUNE:IMM")
                    pk = SA.query('CALC:MARK:Y?')
                    values['Measured power'] = pk[:-1]
                    print(pk)

                    list_of_values.append(values)
    except:
        print('Something went wrong...')

    return list_of_values
    

# open_teraterm()

# try:
#     TT = Application().connect(title="COM5 - Tera Term VT")        
#     terminal = TT.window(title="COM5 - Tera Term VT")        
#     terminal.type_keys("help") # cut this as it is not useful currently
#     terminal.type_keys("{ENTER}")
#     terminal.type_keys("8V_RF_ON")
#     terminal.type_keys("{ENTER}")
#     terminal.type_keys("5V_RF_ON")
#     terminal.type_keys("{ENTER}")
#     terminal.type_keys("3V_RF_ON")
#     terminal.type_keys("{ENTER}")
#     terminal.type_keys("tune_maap")
#     terminal.type_keys("{ENTER}")
#     terminal.type_keys(u"set_point 37", with_spaces=True)
#     terminal.type_keys("{ENTER}")        
#     terminal.type_keys(u"thermal_control on", with_spaces=True)
#     terminal.type_keys("{ENTER}")
#     terminal.type_keys(f"gen_rf 16000 10", with_spaces=True)
#     terminal.type_keys("{ENTER}")

#     time.sleep(1)     
# except:
#     print("Tera Term is not connecting")


serial_module_config()

output=serial_command(serial_port,serial_baudrate,u25_cmd)
output= output.split(" ")
print(output)
u25=float(output[5])
print(u25)
output=serial_command(serial_port,serial_baudrate,u26_cmd)
output= output.split(" ")
u26=float(output[5])
print(u26)
output=serial_command(serial_port,serial_baudrate,u27_cmd)
output= output.split(" ")
u27=float(output[5])
print(u27)

while u25 != -0.5:
    u25_range.append(u25)
    u25 -= 0.5
while u26 != -0.5:
    u26_range.append(u26)
    u26 -= 0.5
while u27 != -0.5:
    u27_range.append(u27)
    u27 -= 0.5

print(u25_range)
print(u26_range)
print(u27_range)


# # DSA()
# df = pd.DataFrame(DSA())
# df.to_csv('DSA_Power_comparison.csv', index=False)
