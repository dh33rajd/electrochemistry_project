
from typing import Dict
import spidev
import smbus
import time
import numpy as np
from settings import *
from utilties import *

spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 1
spi.max_speed_hz=1000000

bus = smbus.SMBus(1)
address = 0x48

scan_rate_label = Label(root,text='Scan rate :')
scan_rate_label.grid(column='1',row='3')

scan_rate = Entry(root)
scan_rate.grid(column='2',row='3',pady=0)

def write_to_register(value, register):
    bus.write_byte_data(address, register, value)

vref = 2.5

register = {
    'BIAS': 17
    }

def set_voltage(voltage: float) -> None:
    REFCN = int(volt_dicc[round(voltage,2)],2)
    #print(REFCN)
    write_to_register(REFCN, register['BIAS'])

def sweep(start_volt:float, stop_volt:float, step:float, TIAG: int,pos: int)-> None:
    wait_time = abs(step/float(scan_rate.get()))
    for voltage in np.arange(start_volt, stop_volt, step):
        # Start timer
        start_time = time.time()
        # Set voltage and read current
        set_voltage(voltage)
        volts, current = read_current(TIAG)
        # Store reading
        DATA_cv[pos]=current
        pos+=1

        # Print output 
        print (" Step: %5.3f\n  Voltage: %5.3f V\m ; Current: %5.3f uA" %(voltage,volts,current))
        
        
        # Stop timer
        time.sleep(wait_time-(time.time() - start_time))
        print("--- %s seconds ---" % (time.time() - start_time))

    
def read_current(TIAG):
    r = spi.readbytes(8)
    #print(r)
    bin_r = r
    bin_r[0] = "{0:08b}".format(r[0])
    bin_r[1] = "{0:08b}".format(r[1])
    bin_r[2] = "{0:08b}".format(r[2])
    bin_r = bin_r[0] + bin_r[1] + bin_r[2]
    bin_r = bin_r[2:18]
    if bin_r[0] == '1':
        aux = bin_r.replace('1', '2').replace('0', '1').replace('2', '0')
        value = -int(aux,2)-1
    else:
        value = int(bin_r,2)

    vmax = 5-(vref/(2**16))
    binmax = ((2**16)-1)
    volts = (vmax*value)/(binmax)+vref
    current = ((volts-(vref/2))/(TIAG))*1000000
    return volts,current


def cyclic_voltammetry(min, max, step,TIAG):
    if((min<max) and step<max-min):
    # forward sweep
        sweep(min, max, step,TIAG,0)
    # backward sweep
        sweep(max, min-step, -step,TIAG,16)
    print(DATA_cv)
            
    a.cla()
    a.grid(True)
    a.set_xlabel('v, V')
    a.set_ylabel('i, '+ u"\u00B5"+'A')
    a.set_title("cyclic voltammetry")
    a.plot(t_cv,DATA_cv,'blue')
    dataPlot.draw()

def start_CV():
    
    #w = Text(root, width='60', height='12', bg='yellow', relief = 'groove')
    #w.grid(column='1',row='9',columnspan='3',rowspan='1',pady=50,padx=20)
    w.delete("1.0","end")
    w.insert('1.0', ">> Transimpedance value selected: {}".format(variable_TIA.get())+'\n'+'\n')
    w.insert('1.0', ">> Operation mode selected: {}".format(variable_OPMODE.get())+'\n'+'\n')
    w.insert('1.0', ">> Starting sweep..."+'\n'+'\n')
    print (">> Transimpedance value selected: {}".format(variable_TIA.get())) 
    print (">> Operation mode selected: {}".format(variable_OPMODE.get()))
    print (">> Starting cyclic voltammetry...")
    
    
    TIA = TIA_dicc["{}".format(variable_TIA.get())]
    TIAG = TIA_values["{}".format(variable_TIA.get())]
    
    LOCK = int('00000000',2)
    TIACN = int(TIA,2)
    REFCN = int('10100101',2)
    MODECN = int('00000011',2)

    write_to_register(LOCK,1)
    write_to_register(TIACN,16)
    write_to_register(REFCN,17)
    write_to_register(MODECN,18)
    
    cyclic_voltammetry(-0.20,0.60,0.05,TIAG)

#startCV()
'''
def main():
    pass

if __name__ == "__main__":
    main()
'''
