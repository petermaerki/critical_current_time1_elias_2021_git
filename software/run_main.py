from mp import pyboard_query

import critical_time

def main():
    ct = critical_time.CritialTime()

    if False:
        button_ms = ct.measure_button_ms()
        print(f'Time between yellow led and button pressed was {button_ms} ms')

    for i in range(20):
        ZERO1_us, TRIP_us, ZERO2_us = ct.measure_times_us(timeout_us = 5e6) # maximum timeout 2e9 us
        diff_us = 0
        if (ZERO1_us is None) or (TRIP_us is None) or (ZERO2_us is None):
            print(f'Timeout. ZERO1_us: {ZERO1_us}, TRIP_us: {TRIP_us},  ZERO2_us: {ZERO2_us}')
            continue

        diff_us = TRIP_us - ZERO1_us # this is the relevant time for Elias
        print(f'Time between slope start and ZERO1_us: {ZERO1_us} and TRIP_us: {TRIP_us}. Difference: {diff_us}. ZERO2_us: {ZERO2_us}')

if __name__ == "__main__":
    main()
