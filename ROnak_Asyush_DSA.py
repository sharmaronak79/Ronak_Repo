import subprocess
import pyvisa
import time
import sys
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import numpy as np
import pandas as pd

# VISA adress of the spectrum analyzer used in this case 
visa_SA = 'TCPIP0::192.168.0.13::inst0::INSTR'
rm = pyvisa.ResourceManager()
time.sleep(2)
SA = rm.open_resource(visa_SA)

freq = 16000

# File path of where the CSV file of the cal data will be stored
filepath = r"C:\Users\crk_lab2\Downloads\DSA_cal_work"

def run():

    # Path where teraterm.exe application is stored
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
        readings = []
        List_of_values = [] # to store dictionary data
        for attenuation in np.linspace(0,0.5,2):
            for frequency in range(2000,17000,1000):
                values = {}
                values['DUT'] = 'BR013-00IV'
                values['DSA'] = '1'
                values['DSA atten (dB)'] = str(attenuation)
                terminal.type_keys(f"gen_rf {frequency} 10", with_spaces=True)
                terminal.type_keys("{ENTER}")
                terminal.type_keys(u"dac_maam 0", with_spaces=True)
                terminal.type_keys("{ENTER}")
                terminal.type_keys(f"dsa_u25 {attenuation}", with_spaces=True)
                terminal.type_keys("{ENTER}")  
                terminal.type_keys(u"dsa_u26 10", with_spaces=True)
                terminal.type_keys("{ENTER}")  
                terminal.type_keys(u"dsa_u27 10", with_spaces=True)
                terminal.type_keys("{ENTER}")

                time.sleep(2)

                SA.write(f'FREQ:CENT {frequency} MHZ')        
                SA.write('*TRG;*WAI')   
                SA.write(":FREQ:TUNE:IMM")
                pk = SA.query('CALC:MARK:Y?')
                readings.append(pk[:-1])
                print(readings)

                if len(readings) >= 15:
                    values['2GHz'] = readings[0]
                    values['3GHz'] = readings[1]
                    values['4GHz'] = readings[2]
                    values['5GHz'] = readings[3]
                    values['6GHz'] = readings[4]
                    values['7GHz'] = readings[5]
                    values['8GHz'] = readings[6]
                    values['9GHz'] = readings[7]
                    values['10GHz'] = readings[8]
                    values['11GHz'] = readings[9]
                    values['12GHz'] = readings[10]
                    values['13GHz'] = readings[11]
                    values['14GHz'] = readings[12]
                    values['15GHz'] = readings[13]
                    values['16GHz'] = readings[14]
                    readings = []
                    print(values)
                    List_of_values.append(values)
                    print(List_of_values)
                #print(str(attenuation) + ',' + str(frequency))

    except:
        print('Something went wrong...')

    return List_of_values

run()

try:
    TT = Application().connect(title="COM5 - Tera Term VT")        
    terminal = TT.window(title="COM5 - Tera Term VT")        
    terminal.type_keys("help") # cut this as it is not useful currently
    terminal.type_keys("{ENTER}")
    terminal.type_keys("8V_RF_ON")
    terminal.type_keys("{ENTER}")
    terminal.type_keys("5V_RF_ON")
    terminal.type_keys("{ENTER}")
    terminal.type_keys("3V_RF_ON")
    terminal.type_keys("{ENTER}")
    terminal.type_keys("tune_maap")
    terminal.type_keys("{ENTER}")
    terminal.type_keys(u"set_point 37", with_spaces=True)
    terminal.type_keys("{ENTER}")        
    terminal.type_keys(u"thermal_control on", with_spaces=True)
    terminal.type_keys("{ENTER}")

    time.sleep(1)     
except:
    print("Tera Term is not connecting")

# DSA()
df = pd.DataFrame(DSA())
df.to_csv('DSA.csv', index=False)
