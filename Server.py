import ctypes
import time

from msl.loadlib import Server32

error_codes = {-5000: 'general communication problem',
    -5001: 'setup file not valid for BTS256',
    -5002: 'setup file could not be opened',
    -5003: 'config file not found',
    -5004: 'az mode out of range (0 - 2 allowed)',
    -5005: 'communication channel can not be opened',
    -5006: 'firmwareversion to low',
    -5007: 'communication send problem',
    -5008: 'communication receive problem',
    -5009: 'device returned error',
    -5010: 'delta uv limit < 0',
    -5014: 'error main data eeprom',
    -5015: 'error color data eeprom',
    -5017: 'error zero adjust integral amplifier',
    -5020: 'error dark current measurement',
    -5023: 'error BTS256 overload',
    -5024: 'error user data eeprom',
    -5997: 'no BTS256 connected',
    -5998: 'device connected with different serial number',
    -5999: 'unknown error'}


class Optik(Server32):
    
    def __init__(self, host, port, quiet, **kwargs):
        Server32.__init__(self, 'GOMDBTS256.dll', 'windll', host, port, quiet)
        
        self._handle = None
        self.name = 'BTS256_'+kwargs['serial'].rstrip('M')
        self.get_handle(self.name)

    def _check_return(self, ret):
        if ret != 0:
            raise ValueError(error_codes[ret]) 
     
    def get_handle(self, name):
        handle = ctypes.c_int()
        self._check_return(self.lib.GOMDBTS256_getHandle(ctypes.c_char_p(name.encode()), ctypes.byref(handle)))
        self._handle = handle.value
        
    def release_handle(self):
        self._check_return(self.lib.GOMDBTS256_releaseHandle(self._handle))

    def show_config(self,control):
        application_handle = 0
        controlbits = ctypes.c_int(control)
        self._check_return(self.lib.GOMDBTS256_showConfig(self._handle, application_handle, controlbits))

    def integral_enabled(self):
        enabled = ctypes.c_bool()
        self._check_return(self.lib.GOMDBTS256_integralIsEnabled(self._handle, ctypes.byref(enabled)))
        return enabled.value

    def set_integral(self,set):
        enable = ctypes.c_bool(set)
        self._check_return(self.lib.GOMDBTS256_integralSetEnabled(self._handle, enable))

    def set_spectral(self,set):
        enable = ctypes.c_bool(set)
        self._check_return(self.lib.GOMDBTS256_spectralSetEnabled(self._handle, enable))

    def spectral_get_integration_time(self):
        integration_time = ctypes.c_int()
        self._check_return(self.lib.GOMDBTS256_spectralGetIntegrationTimeInMs(self._handle, ctypes.byref(integration_time)))
        return integration_time.value

    def spectral_set_integration_time(self, ms):
        integration_time = ctypes.c_int(ms)
        self._check_return(self.lib.GOMDBTS256_spectralSetIntegrationTimeInMs(self._handle, integration_time))

    def spectral_set_integration_maxtime(self, ms):
        max_integration_time = ctypes.c_int(ms)
        self._check_return(self.lib.GOMDBTS256_spectralSetIntegrationTimeMaxInMs(self._handle, max_integration_time))

    def spectral_get_integration_maxtime(self):
        max_integration_time = ctypes.c_int()
        self._check_return(self.lib.GOMDBTS256_spectralGetIntegrationTimeMaxInMs(self._handle, ctypes.byref(max_integration_time)))
        return max_integration_time.value

    def integral_get_integration_time(self):
        integration_time = ctypes.c_int()
        self._check_return(self.lib.GOMDBTS256_integralGetIntegrationTimeInMs(self._handle, ctypes.byref(integration_time)))
        return integration_time.value

    def integral_set_integration_time(self, ms):
        integration_time = ctypes.c_int(ms)
        self._check_return(self.lib.GOMDBTS256_integralSetIntegrationTimeInMs(self._handle, integration_time))

    def integral_get_synchronization(self):
        sync = ctypes.c_int()
        self._check_return(self.lib.GOMDBTS256_integralGetSynchronization(self._handle, ctypes.byref(sync)))
        return sync.value

    def integral_set_synchronization(self,sync):
        sync = ctypes.c_int(sync)
        self._check_return(self.lib.GOMDBTS256_integralSetSynchronization(self._handle, sync))

    def get_temperature(self):
        temperature = ctypes.c_double()
        self._check_return(self.lib.GOMDBTS256_getTemperature(self._handle, ctypes.byref(temperature)))
        return temperature.value
        
    #def get_CRI(self):
        #Ra = ctypes.c_double()
        #R1 = ctypes.c_double()
        #R2 = ctypes.c_double()
        #R3 = ctypes.c_double()
        #R4 = ctypes.c_double()
        #R5 = ctypes.c_double()
        #R6 = ctypes.c_double()
        #R7 = ctypes.c_double()
        #R8 = ctypes.c_double()
        #R9 = ctypes.c_double()
        #R10 = ctypes.c_double()
        #R11 = ctypes.c_double()
        #R12 = ctypes.c_double()
        #R13 = ctypes.c_double()
        #R14 = ctypes.c_double()
        #CRI = (Ra, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14)
        #get_CRI = (ctypes.c_double * CRI)()
        #self._check_return(self.lib.GOMDBTS256_getCRI(self._handle, ctypes.byref(Ra), ctypes.byref(R1), ctypes.byref(R2), ctypes.byref(R3), ctypes.byref(R4), ctypes.byref(R5), ctypes.byref(R6), ctypes.byref(R7), ctypes.byref(R8), ctypes.byref(R9), ctypes.byref(R10), ctypes.byref(R11), ctypes.byref(R12), ctypes.byref(R3), ctypes.byref(R14))
        #return [Ra.value, R1.value, R2.value, R3.value, R4.value, R5.value, R6.value, R7.value, R8.value, R9.value, R10.value, R11.value, R12.value, R13.value, R14.value]
        
        #return Ra, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14
    
    #get_CRI[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    
    def spectral_get_spec_max(self):
        spectral_get_spec_max = ctypes.c_int()
        self._check_return(self.lib.GOMDBTS256_spectralGetSpecmax(self._handle, ctypes.byref(spectral_get_spec_max)))
        return spectral_get_spec_max.value
        
    def get_wavelength_range(self):
        min_wavelength = ctypes.c_double()
        max_wavelength = ctypes.c_double()
        step_width = ctypes.c_double()
        self._check_return(self.lib.GOMDBTS256_getWavelengthRange(self._handle, ctypes.byref(min_wavelength),
                                                                ctypes.byref(max_wavelength), ctypes.byref(step_width)))
        return min_wavelength.value, max_wavelength.value, step_width.value

    def set_wavelength_range(self):  # set wavelength range and step width (nm), standard is 380, 758.26, 1
        min_wavelength = ctypes.c_double(380)
        max_wavelength = ctypes.c_double(758)
        step_width = ctypes.c_double(1)
        self._check_return(self.lib.GOMDBTS256_setWavelengthRange(self._handle, min_wavelength,
                                                                  max_wavelength, step_width))
        return

    def get_counts_wavelength(self):
        get_counts_wavelength = (ctypes.c_double * 379)()  # 379
        self._check_return(self.lib.GOMDBTS256_spectralGetCountsWavelength(self._handle,
                                                                           ctypes.byref(get_counts_wavelength)))
        return [val for val in get_counts_wavelength]

    def measure(self):
        self._check_return(self.lib.GOMDBTS256_measure(self._handle))
        return

    def get_cwvalue(self):
        measured = ctypes.c_double()
        self._check_return(self.lib.GOMDBTS256_getCWValue(self._handle, ctypes.byref(measured)))
        return measured.value

    def get_colour(self):
        UpperX = ctypes.c_double()
        UpperY = ctypes.c_double()
        UpperZ = ctypes.c_double()
        x = ctypes.c_double()
        y = ctypes.c_double()
        us = ctypes.c_double()
        vs = ctypes.c_double()
        CCT = ctypes.c_double()
        domWL = ctypes.c_double()
        self._check_return(self.lib.GOMDBTS256_getColor(self._handle, ctypes.byref(UpperX), ctypes.byref(UpperY),
                                                        ctypes.byref(UpperZ), ctypes.byref(x), ctypes.byref(y),
                                                        ctypes.byref(us), ctypes.byref(vs), ctypes.byref(CCT),
                                                        ctypes.byref(domWL)))
        return UpperX.value, UpperY.value, UpperZ.value, x.value, y.value, us.value, vs.value, CCT.value, domWL.value

    def get_counts_pixel(self):
        get_counts_pixel = (ctypes.c_double * 256)()
        self._check_return(self.lib.GOMDBTS256_spectralGetCountsPixel(self._handle, ctypes.byref(get_counts_pixel)))
        return [val for val in get_counts_pixel]

    def display_light(self):
        light_on = ctypes.c_bool(False)  # True -> display back lit, False otherwise
        self._check_return(self.lib.GOMDBTS256_switchLight(self._handle, light_on))
        return

    def get_calnum(self):
        calnum = ctypes.c_int()
        self._check_return(self.lib.GOMDBTS256_getSelectedCalibrationEntryNumber(self._handle, ctypes.byref(calnum)))
        return calnum.value

    def set_calnum(self,calnum):
        calnum = ctypes.c_int(calnum)
        self._check_return(self.lib.GOMDBTS256_setCalibrationEntryNumber(self._handle, calnum))

    def get_quantity(self,calnum):
        quantity = ctypes.create_string_buffer(10)
        calentry = ctypes.c_int(calnum)
        self._check_return(self.lib.GOMDBTS256_getMeasurementQuantity(self._handle, calentry, ctypes.byref(quantity)))
        return quantity.value.decode()

    def integral_get_unit(self,calnum):
        unit = ctypes.create_string_buffer(10)
        calentry = ctypes.c_int(calnum)
        self._check_return(self.lib.GOMDBTS256_integralGetUnit(self._handle, calentry, ctypes.byref(unit)))
        return unit.value.decode()

    def set_azmode(self,mode):
        option = ctypes.c_int(mode)
        self._check_return(self.lib.GOMDBTS256_integralSetAzMode(self._handle, option))

