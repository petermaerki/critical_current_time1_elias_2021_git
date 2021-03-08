import pyb
import micropython
micropython.alloc_emergency_exception_buf(100)

class MpCriticalTime:
    def __init__(self):
        self._red = pyb.LED(1)
        self._green = pyb.LED(2)
        self._yellow = pyb.LED(3)
        self._button = pyb.Switch()
        self._button.callback(self._button_pressed)

        self.opto_fet_R = pyb.Pin(pyb.Pin.board.X6, pyb.Pin.OUT_PP)
        self.opto_fet_S = pyb.Pin(pyb.Pin.board.X4, pyb.Pin.OUT_PP)
        # PA0, PB0, PC0, PD0, etc all connect to line 0.
        # PA1, PB1, PC1, PD1, etc all connect to line 1.
        # etc
        # PA15, PB15, PC15, PD15 all connect to line 15.
        self._pinZERO = pyb.ExtInt(pyb.Pin.board.X1, pyb.ExtInt.IRQ_RISING_FALLING, pyb.Pin.PULL_NONE , self._pinZERO_callback)
        self._pinTRIP = pyb.ExtInt(pyb.Pin.board.X2, pyb.ExtInt.IRQ_RISING_FALLING, pyb.Pin.PULL_NONE , self._pinTRIP_callback)
        self.reset()
    
    def reset(self):
        self._red.off()
        self._green.off()
        self._yellow.off()
        self.opto_fet_R.value(1)
        self.opto_fet_S.value(0)
        self._pinZERO.disable()
        self._pinTRIP.disable()

    def measure_button_ms(self):
        self.button_ms = None
        self._yellow.on()
        self.start_ms = pyb.millis()

        while (self.button_ms is None) and (pyb.elapsed_millis(self.start_ms) < 5000):
            pyb.delay(100) # ms

        self._yellow.off()
        return self.button_ms

    def measure_times_us(self, timeout_us = 5e6):
        self.ZERO1_us = None
        self.TRIP_us = None
        self.ZERO2_us = None

        # opto_fet, start slope
        self.opto_fet_R.value(0)
        pyb.delay(1) # ms   make shure R is open
        self.opto_fet_S.value(1) # slope starts
        self.start_us = pyb.micros()
        self._pinZERO.enable()


        while ((self.ZERO1_us is None) or (self.TRIP_us is None) or (self.ZERO2_us is None)) and (pyb.elapsed_micros(self.start_us) < timeout_us):
            pyb.delay(1) # ms

        self.reset()
        return self.ZERO1_us, self.TRIP_us, self.ZERO2_us,

    def _button_pressed(self):
        self.button_ms = pyb.elapsed_millis(self.start_ms)
        self._yellow.off()
        self._green.on()

    def _pinZERO_callback(self, _line):
        us = pyb.elapsed_micros(self.start_us)
        if self.ZERO1_us == None: # first time
            self.ZERO1_us = us
            self._pinZERO.disable()
            #self._pinZERO.regs()  # dump register values
            self._pinTRIP.enable()
        if (self.ZERO1_us and self.TRIP_us) and (self.ZERO2_us == None):
            self.ZERO2_us = us
            self._pinZERO.disable()


    def _pinTRIP_callback(self, _line):
        us = pyb.elapsed_micros(self.start_us)
        if self.TRIP_us == None:
            self.TRIP_us = us
        self._pinTRIP.disable()
        self._pinZERO.enable() 
        self.opto_fet_R.value(1)
        self.opto_fet_S.value(0)


singleton = MpCriticalTime()
