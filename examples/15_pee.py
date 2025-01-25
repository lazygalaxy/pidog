#!/usr/bin/env python3
import time
from pidog import Pidog
from time import sleep
from preset_actions import howling

my_dog = Pidog()

sleep(0.5)

stand = my_dog.legs_angle_calculation([[0, 80], [0, 80], [30, 75], [30, 75]])
pee = my_dog.legs_angle_calculation([[0, 80], [0, 80], [30, 75], [75, 75]])


def pee():
    my_dog.legs_move([stand], speed=70)
    my_dog.wait_all_done()
    my_dog.legs_move([pee], speed=50)
    my_dog.wait_all_done()
    time.sleep(3.0)


if __name__ == "__main__":
    try:
        while True:
            pee()
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\033[31mERROR: {e}\033[m")
    finally:
        my_dog.close()
