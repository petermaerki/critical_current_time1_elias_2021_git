from mp import pyboard_query

import critical_time

def main():
    ct = critical_time.CritialTime()

    if False:
        button_ms = ct.measure_button_ms()
        print(f'Time between yellow led and button pressed was {button_ms} ms')

    for i in range(20):
        ZERO_us, TRIP_us = ct.measure_times_us(timeout_us = 5e6) # maximum timeout 2e9 us
        diff_us = 0
        if ZERO_us and TRIP_us:
            diff_us = TRIP_us - ZERO_us
        print(f'Time between slope start and ZERO: {ZERO_us} and TRIP: {TRIP_us}. Difference: {diff_us} ')


if __name__ == "__main__":
    main()
