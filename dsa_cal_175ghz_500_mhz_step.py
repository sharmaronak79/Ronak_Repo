import pyvisa
import time
import sys
import numpy as np
import pandas as pd
import serial

visa_SA = 'TCPIP0::192.168.10.13::inst0::INSTR'
rm = pyvisa.ResourceManager()
time.sleep(2)
SA = rm.open_resource(visa_SA)

serial_port = 'COM5'
serial_baudrate = 115200
timeout = 5
sn_cmd = 'show\n'

# Variable which dictates how long delay in between reading on the spectrum analyzer is
delay = 0.8

def serial_command(port, baudrate, command, timeout=5):
    try:
        # Open the serial port
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            # Give some time for the serial connection to establish
            time.sleep(1)
            
            # Flush any existing input/output
            ser.flushInput()
            ser.flushOutput()
            
            # Send the command to the device
            ser.write((command + '\r').encode())
            
            
            # Wait for a response
            time.sleep(0.5)
            
            # Read the response
            response = ser.read_all().decode().strip()
            
            return response
    except serial.SerialException as e:
        return f"Serial error: {e}"
    except Exception as e:
        return f"Error: {e}"

    
def serial_module_config(port, baudrate, timeout) -> str:
    """
    Configures the RF module with its default settings

    port: str → Specifies which communications port you have connected for data transfer

    baudrate: int → Rate at which information is transferred in the com port

    timeout: int → Value at which you wish to time out in case nothing happens
    """
    try:
        # Open the serial port
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            # Give some time for the serial connection to establish
            time.sleep(1)
            
            # Flush any existing input/output
            ser.flushInput()
            ser.flushOutput()
            
            # Send the command to the device
            ser.write(("\n"+ '\r').encode())
            time.sleep(0.2)
            ser.write(("8V_RF_ON\n"+ '\r').encode())
            time.sleep(0.2)
            ser.write(("5V_RF_ON\n"+ '\r').encode())
            time.sleep(0.2)
            ser.write(("3V_RF_ON\n"+ '\r').encode())
            time.sleep(0.2)
            ser.write(("tune_maap\n"+ '\r').encode())
            time.sleep(1)
            ser.write(("set_point 37\n"+ '\r').encode())
            time.sleep(0.2)
            ser.write(("thermal_control on\n"+ '\r').encode())
            
            # Read the response
            response = ser.read_all().decode().strip()
            
            return response
        
    except serial.SerialException as e:
        return f"Serial error: {e}"
    except Exception as e:
        return f"Error: {e}"
    

def DSA(serial_number):
    try:
        print('Connecting to Spectrum Analyzer...')
        SA = rm.open_resource(visa_SA)
        SA.timeout = 5000

    except:
        print('Cannot connect to Spectrum Analyzer. Exiting now...')
        sys.exit()

    else:
        print('Spectrum Analyzer connected')

        SA.write('CALC:MARK:CPS ON')
        SA.write('BANDwidth:RESolution 240')
        SA.write('FREQ:SPAN 25000')
        SA.write('DISP:WIND:TRAC:Y:RLEV 20 dBm')
        SA.write(':POWer:ATTenuation 30')
        SA.write('INIT:CONT 0')
        SA.write('INIT:IMM')
        
    try:
        # Open the serial port
        with serial.Serial(port='COM5', baudrate=115200, timeout=timeout) as ser:
            # Give some time for the serial connection to establish
            time.sleep(1)
            
            # Flush any existing input/output
            ser.flushInput()
            ser.flushOutput()
            readings = []
            List_of_values = [] # to store dictionary data
            print('SN: ' + serial_number)
            ser.write((f'squelch off' + '\r').encode())
            time.sleep(delay)
            for attenuation in np.linspace(0,31.5,64):
                for frequency in range(2000,18000,500):
                    values = {}
                    values['DUT'] = serial_number
                    values['DSA'] = '1'
                    values['DSA atten (dB)'] = str(attenuation)
                    #serial_command_DSA(serial_port, serial_baudrate, timeout, attenuation, frequency)
                    # Send the command to the device
                    ser.write((f'gen_rf {frequency} 10\n' + '\r').encode())
                    ser.write((f'dsa_u25 {attenuation}\n' + '\r').encode())
                    ser.write((f'dsa_u26 10\n' + '\r').encode())
                    ser.write((f'dsa_u27 10\n' + '\r').encode())
                
                    # Wait for a response
                    #time.sleep(1)
                    
                    # Read the response
                    response = ser.read_all().decode().strip()
                    SA.write(f'FREQ:CENT {frequency} MHz')
                    SA.write('*trg;*wai')
                    time.sleep(delay)
                    pk = SA.query('CALC:MARK:Y?')
                    pk = float(pk)
                    readings.append(pk)
                    print(readings)
                    

                    if len(readings) >= 32: # for 16000, it was 142
                        values['2000 MHz'] = readings[0]
                        values['2500 MHz'] = readings[1]
                        values['3000 MHz'] = readings[2]
                        values['3500 MHz'] = readings[3]
                        values['4000 MHz'] = readings[4]
                        values['4500 MHz'] = readings[5]
                        values['5000 MHz'] = readings[6]
                        values['5500 MHz'] = readings[7]
                        values['6000 MHz'] = readings[8]
                        values['6500 MHz'] = readings[9]
                        values['7000 MHz'] = readings[10]
                        values['7500 MHz'] = readings[11]
                        values['8000 MHz'] = readings[12]
                        values['8500 MHz'] = readings[13]
                        values['9000 MHz'] = readings[14]
                        values['9500 MHz'] = readings[15]
                        values['10000 MHz'] = readings[16]
                        values['10500 MHz'] = readings[17]
                        values['11000 MHz'] = readings[18]
                        values['11500 MHz'] = readings[19]
                        values['12000 MHz'] = readings[20]
                        values['12500 MHz'] = readings[21]
                        values['13000 MHz'] = readings[22]
                        values['13500 MHz'] = readings[23]
                        values['14000 MHz'] = readings[24]
                        values['14500 MHz'] = readings[25]
                        values['15000 MHz'] = readings[26]
                        values['15500 MHz'] = readings[27]
                        values['16000 MHz'] = readings[28]
                        values['16500 MHz'] = readings[29]
                        values['17000 MHz'] = readings[30]
                        values['17500 MHz'] = readings[31]

                        readings = []
                        print(values)
                        List_of_values.append(values)
                        print(List_of_values)
                        #print(str(attenuation) + ',' + str(frequency))

            for attenuation in np.linspace(0,31.5,64):
                for frequency in range(2000,17000,1000):
                    values = {}
                    values['DUT'] = serial_number
                    values['DSA'] = '2'
                    values['DSA atten (dB)'] = str(attenuation)
                    #serial_command_DSA(serial_port, serial_baudrate, timeout, attenuation, frequency)
                    # Send the command to the device
                    ser.write((f'gen_rf {frequency} 10\n' + '\r').encode())
                    ser.write((f'dsa_u25 10\n' + '\r').encode())
                    ser.write((f'dsa_u26 {attenuation}\n' + '\r').encode())
                    ser.write((f'dsa_u27 10\n' + '\r').encode())
                    
                    # Wait for a response
                    #time.sleep(1)
                    
                    # Read the response
                    response = ser.read_all().decode().strip()
                    SA.write(f'FREQ:CENT {frequency} MHz')
                    SA.write('*trg;*wai')
                    time.sleep(delay)
                    pk = SA.query('CALC:MARK:Y?')
                    pk = float(pk)
                    readings.append(pk)
                    print(readings)
                    

                    if len(readings) >= 32: # 140 
                        values['2000 MHz'] = readings[0]
                        values['2500 MHz'] = readings[1]
                        values['3000 MHz'] = readings[2]
                        values['3500 MHz'] = readings[3]
                        values['4000 MHz'] = readings[4]
                        values['4500 MHz'] = readings[5]
                        values['5000 MHz'] = readings[6]
                        values['5500 MHz'] = readings[7]
                        values['6000 MHz'] = readings[8]
                        values['6500 MHz'] = readings[9]
                        values['7000 MHz'] = readings[10]
                        values['7500 MHz'] = readings[11]
                        values['8000 MHz'] = readings[12]
                        values['8500 MHz'] = readings[13]
                        values['9000 MHz'] = readings[14]
                        values['9500 MHz'] = readings[15]
                        values['10000 MHz'] = readings[16]
                        values['10500 MHz'] = readings[17]
                        values['11000 MHz'] = readings[18]
                        values['11500 MHz'] = readings[19]
                        values['12000 MHz'] = readings[20]
                        values['12500 MHz'] = readings[21]
                        values['13000 MHz'] = readings[22]
                        values['13500 MHz'] = readings[23]
                        values['14000 MHz'] = readings[24]
                        values['14500 MHz'] = readings[25]
                        values['15000 MHz'] = readings[26]
                        values['15500 MHz'] = readings[27]
                        values['16000 MHz'] = readings[28]
                        values['16500 MHz'] = readings[29]
                        values['17000 MHz'] = readings[30]
                        values['17500 MHz'] = readings[31]

                        readings = []
                        print(values)
                        List_of_values.append(values)
                        print(List_of_values)
                        #print(str(attenuation) + ',' + str(frequency))
            for attenuation in np.linspace(0,31.5,64):
                for frequency in range(2000,17000,1000):
                    values = {}
                    values['DUT'] = serial_number
                    values['DSA'] = '3'
                    values['DSA atten (dB)'] = str(attenuation)
                    #serial_command_DSA(serial_port, serial_baudrate, timeout, attenuation, frequency)
                    # Send the command to the device
                    ser.write((f'gen_rf {frequency} 10\n' + '\r').encode())
                    ser.write((f'dsa_u25 10\n' + '\r').encode())
                    ser.write((f'dsa_u26 10\n' + '\r').encode())
                    ser.write((f'dsa_u27 {attenuation}\n' + '\r').encode())
                
                    # Wait for a response
                    #time.sleep(1)
                    
                    # Read the response
                    response = ser.read_all().decode().strip()
                    SA.write(f'FREQ:CENT {frequency} MHz')
                    SA.write('*trg;*wai')
                    time.sleep(delay)
                    pk = SA.query('CALC:MARK:Y?')
                    pk = float(pk)
                    readings.append(pk)
                    print(readings)
                    

                    if len(readings) >= 32: # 140 
                        values['2000 MHz'] = readings[0]
                        values['2500 MHz'] = readings[1]
                        values['3000 MHz'] = readings[2]
                        values['3500 MHz'] = readings[3]
                        values['4000 MHz'] = readings[4]
                        values['4500 MHz'] = readings[5]
                        values['5000 MHz'] = readings[6]
                        values['5500 MHz'] = readings[7]
                        values['6000 MHz'] = readings[8]
                        values['6500 MHz'] = readings[9]
                        values['7000 MHz'] = readings[10]
                        values['7500 MHz'] = readings[11]
                        values['8000 MHz'] = readings[12]
                        values['8500 MHz'] = readings[13]
                        values['9000 MHz'] = readings[14]
                        values['9500 MHz'] = readings[15]
                        values['10000 MHz'] = readings[16]
                        values['10500 MHz'] = readings[17]
                        values['11000 MHz'] = readings[18]
                        values['11500 MHz'] = readings[19]
                        values['12000 MHz'] = readings[20]
                        values['12500 MHz'] = readings[21]
                        values['13000 MHz'] = readings[22]
                        values['13500 MHz'] = readings[23]
                        values['14000 MHz'] = readings[24]
                        values['14500 MHz'] = readings[25]
                        values['15000 MHz'] = readings[26]
                        values['15500 MHz'] = readings[27]
                        values['16000 MHz'] = readings[28]
                        values['16500 MHz'] = readings[29]
                        values['17000 MHz'] = readings[30]
                        values['17500 MHz'] = readings[31]

                        readings = []
                        print(values)
                        List_of_values.append(values)
                        print(List_of_values)
                        #print(str(attenuation) + ',' + str(frequency))
            return List_of_values
        
    except serial.SerialException as e:
        return f"Serial error: {e}"
    except Exception as e:
        return f"Error: {e}"

serial_number_data = serial_command(serial_port, serial_baudrate, sn_cmd)
serial_number_data = serial_number_data.split(" ")
serial_number = str(serial_number_data[12])
serial_number = serial_number[:-7]
#print('SN: ' + serial_number)

serial_module_config(serial_port, serial_baudrate, timeout)

path = r'C:\FT_Share\Reports\DSA Calibration'
df = pd.DataFrame(DSA(serial_number))
df.to_csv(path + f'\\DSA_cal_{serial_number}.csv', index=False)
print(f'File saved succesfully as DSA_cal_{serial_number}.csv')
