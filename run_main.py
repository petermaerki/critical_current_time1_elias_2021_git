from mp import pyboard_query

import critical_time

def main():
    ct = critical_time.CritialTime()
    button_ms = ct.measure_button_ms()
    print(f'Time between yellow led and button pressed was {button_ms} ms')

    A_us, B_us = ct.measure_times_us()
    print(f'Time between trigger output and edge A/B  was {A_us}/{B_us} us')

if __name__ == "__main__":
    main()
