from datetime import datetime

from msl.qt import QtWidgets, QtCore, prompt
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

file ='TechRentals cal.csv'

ref_plane_count = 0
lux_count = 0
CCT_count = 0

print('ready')

with open(file,mode='a') as fp:
    fp.write('\n' + datetime.now().replace(microsecond=0).isoformat(sep=' ')+'\n')


def r_pressed():
    global ref_plane_count
    with open(file, mode='a') as fp:
        text = prompt.text('Enter distance (m)', title=None, font=24, value='', multi_line=False, echo=0)
        if not text:
            return
        optik.set_spectral(False)
        ref_plane_count += 1
        z = []
        lux = [f'{text} m run {ref_plane_count:02}']
        # fp.write('\n')
        for i in range(lux_measurements):
            optik.measure()
            print(optik.get_cwvalue())
            lux.append(str(optik.get_cwvalue()))
            z.append(optik.get_cwvalue())
        a = sum(z) / 10
        print('Mean: {}'.format(a))
        fp.write(','.join(lux) + '\n')
        print('done')


def t_pressed():
    optik.set_spectral(False)
    z = []
    for i in range(lux_measurements):
        optik.measure()
        print(optik.get_cwvalue())
        z.append(optik.get_cwvalue())
    a = sum(z) / 10
    print('Mean: {}'.format(a))
    print('done')

def l_pressed():
    global lux_count
    with open(file, mode='a') as fp:
        text = prompt.text('Enter lux value (lx)', title=None, font=24, value='', multi_line=False, echo=0)
        if not text:
            return
        optik.set_spectral(False)
        #optik.set_spectral(True)
        lux_count += 1
        z = []
        lux = [f'{text} lux run {lux_count:02}']
        # fp.write('\n')
        for i in range(lux_measurements):
            optik.measure()
            print(optik.get_cwvalue())
            lux.append(str(optik.get_cwvalue()))
            z.append(optik.get_cwvalue())
        a = sum(z) / 10
        print('Mean: {}'.format(a))
        fp.write(','.join(lux)+'\n')
        print('done')

def c_pressed():
    global CCT_count
    with open(file, mode='a') as fp:
        text = prompt.text('Enter lux value/distance ', title=None, font=24, value='', multi_line=False, echo=0)
        if not text:
            return
        optik.set_spectral(True)
        CCT_count += 1
        z = []
        colour = [f'CCT run {CCT_count:02} at {text}']
        # fp.write('\n')
        for i in range(CCT_measurements):
            optik.measure()
            print(optik.get_colour()[7])
            colour.append(str(optik.get_colour()[7]))
            z.append(optik.get_colour()[7])
        a = sum(z) / 5
        print('Mean: {}'.format(a))
        fp.write(','.join(colour) + '\n')
        print('done')


class BlackScreen(QtWidgets.QWidget):

    def __init__(self):
        """Make the desktop screen black."""
        super(BlackScreen, self).__init__()
        self.setWindowTitle('Press Esc to toggle')
        self.setStyleSheet('background-color:black;color:white')
        self.showMaximized()

    def black(self):
        self.showFullScreen()

    def toggle(self):
        """Toggle between full screen and normal display."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def keyPressEvent(self, event):
        """Overrides :meth:`QtWidgets.QtWidget.keyPressEvent`."""
        super(BlackScreen, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Escape:
            self.toggle()
        elif event.key() == QtCore.Qt.Key_T:
            t_pressed()
        elif event.key() == QtCore.Qt.Key_R:
            self.toggle()
            r_pressed()
            self.toggle()
        elif event.key() == QtCore.Qt.Key_C:
            self.toggle()
            c_pressed()
            self.toggle()
        elif event.key() == QtCore.Qt.Key_L:
            self.toggle()
            l_pressed()
            self.toggle()


app = QtWidgets.QApplication()
bs = BlackScreen()
bs.show()
app.exec()

optik.release_handle()