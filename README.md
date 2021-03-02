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
ct = critical_time.CritialTime()
A_us, B_us = ct.measure_times_us()
print(f'Time between trigger output and edge A/B  was {A_us}/{B_us} us')
```

A output pin will trigger a process which then will trigger edge A and edge B.
The time between trigger and edge A and B will be printed to the console.
