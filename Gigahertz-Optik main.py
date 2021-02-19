import time
from datetime import datetime
import keyboard
import os
from msl.qt import prompt

from Controller import Optik64

serial = '14195'
dll_folder = r'C:\Users\y.tan\GigaHertz Lux Meter\S-SDK-BT256\runtime'
optik = Optik64(dll_folder, serial)

lux_measurements = 10
CCT_measurements = 5
spectral_time = 0   # device calculates best spectral integration time based on signal
max_spectral_time = 5000
integral_time = 1000
calnum = optik.get_calnum()
sync = 0
az_mode = 0     # 0 = no correction; 1 = set with specific factor; 2 = dynamic factor with array measurement

optik.integral_set_integration_time(integral_time)
optik.spectral_set_integration_time(spectral_time)
optik.spectral_set_integration_maxtime(max_spectral_time)
optik.set_azmode(az_mode)
# optik.integral_set_synchronization(sync)
# print(optik.integral_get_synchronization())

# print(optik.integral_get_unit(calnum))

# print(optik.get_quantity(calnum))
# if optik.get_quantity(calnum) != 'E':
#     raise ValueError('not measuring illuminance')

file ='GlycoSyn_Precision Air_cal.csv'

ref_plane_count = 0
lux_count = 0
CCT_count = 0

print('ready')

with open(file,mode='a') as fp:
    fp.write('\n' + datetime.now().replace(microsecond=0).isoformat(sep=' ')+'\n')
while True:
    if keyboard.is_pressed('t'):
        optik.set_spectral(False)
        for i in range(lux_measurements):
            optik.measure()
            print(optik.get_cwvalue())
        print('done')
    if keyboard.is_pressed('r'):
        with open(file, mode='a') as fp:
            text = prompt.text('Enter distance (m)', title=None, font=24, value='', multi_line=False, echo=0)
            if not text: continue
            optik.set_spectral(False)
            ref_plane_count += 1
            lux = [f'{text} m run {ref_plane_count:02}']
            # fp.write('\n')
            for i in range(lux_measurements):
                optik.measure()
                print(optik.get_cwvalue())
                lux.append(str(optik.get_cwvalue()))
            fp.write(','.join(lux)+'\n')
            print('done')
    if keyboard.is_pressed('l'):
        with open(file, mode='a') as fp:
            text = prompt.text('Enter lux value (lx)', title=None, font=24, value='', multi_line=False, echo=0)
            if not text: continue
            optik.set_spectral(False)
            #optik.set_spectral(True)
            lux_count += 1
            lux = [f'{text} lux run {lux_count:02}']
            # fp.write('\n')
            for i in range(lux_measurements):
                optik.measure()
                print(optik.get_cwvalue())
                lux.append(str(optik.get_cwvalue()))
            fp.write(','.join(lux)+'\n')
            print('done')
    if keyboard.is_pressed(('c')):
        with open(file, mode='a') as fp:
            text = prompt.text('Enter lux value/distance ', title=None, font=24, value='', multi_line=False, echo=0)
            if not text: continue
            optik.set_spectral(True)
            CCT_count += 1
            colour = [f'CCT run {CCT_count:02} at {text}']
            # fp.write('\n')
            for i in range(CCT_measurements):
                optik.measure()
                print(optik.get_colour()[7])
                colour.append(str(optik.get_colour()[7]))
            fp.write(','.join(colour) + '\n')
            print('done')
    elif keyboard.is_pressed('s'):
        break

optik.release_handle()