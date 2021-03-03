import pyb

class MpCriticalTime:
    def __init__(self):
        self._red = pyb.LED(1)
        self._green = pyb.LED(2)
        self._yellow = pyb.LED(3)
        self._button = pyb.Switch()
        self._button.callback(self._button_pressed)
        # PA0, PB0, PC0, PD0, etc all connect to line 0.
        # PA1, PB1, PC1, PD1, etc all connect to line 1.
        # etc
        # PA15, PB15, PC15, PD15 all connect to line 15.
        self._pinA = pyb.ExtInt(pyb.Pin.board.X1, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, self._pinA_callback)
        self._pinB = pyb.ExtInt(pyb.Pin.board.X2, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, self._pinB_callback)
    
    def reset(self):
        self._red.off()
        self._green.off()
        self._yellow.off()

    def measure_button_ms(self):
        self.button_ms = None
        self._yellow.on()
        self.start_ms = pyb.millis()

        while (self.button_ms is None) and (pyb.elapsed_millis(self.start_ms) < 5000):
            pyb.delay(100) # ms

        self._yellow.off()
        return self.button_ms

    def measure_times_us(self, timeout_us = 5e6):
        self.A_us = None
        self.B_us = None

        self._pinA.enable()
        # fet ansteuern
        self.start_us = pyb.micros()

        while ((self.A_us is None) or (self.B_us is None)) and (pyb.elapsed_micros(self.start_us) < timeout_us):
            pyb.delay(1) # ms

        return self.A_us, self.B_us

    def _button_pressed(self):
        self.button_ms = pyb.elapsed_millis(self.start_ms)
        self._yellow.off()
        self._green.on()

    def _pinA_callback(self):
        self.A_us = pyb.elapsed_micros(self.start_us)
        self._pinA.disable()

    def _pinB_callback(self):
        self.B_us = pyb.elapsed_micros(self.start_us)
        self._pinB.disable()

singleton = MpCriticalTime()
