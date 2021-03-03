# critical_current_time1_elias_2021

Voltage ramp generator and time measurement with pyboard to measure the critical current of a supraconductive device.

## Test using Button

```python
ct = critical_time.CritialTime()
button_ms = ct.measure_button_ms()
print(f'Time between yellow led and button pressed was {button_ms} ms')
```

When starting this program, the yellow led will glare.
Press the USR-Button and the green led will glare.
The time will be printed on the console.


## Measuring time between trigger and two feedbacks

```python
ZERO1_us, TRIP_us, ZERO2_us = ct.measure_times_us(timeout_us = 5e6) # maximum timeout 2e9 us
```

Opto Fets are used to start the slope.
Times are measured in us:
- first crossing of 0V: ZERO1_us
- Trip of supraconductive device: TRIP_us
Opto Fets are set to go back to the start voltge
- secont crossing of 0V: ZERO2_us
