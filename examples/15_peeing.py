#!/usr/bin/env python3
import time
from pidog import Pidog
from preset_actions import bark

my_dog = Pidog()

stand = my_dog.legs_angle_calculation([[0, 80], [0, 80], [30, 75], [30, 75]])
left_pipi = my_dog.legs_angle_calculation([[0, 40], [0, 80], [30, 75], [30, 0]])
right_pipi = my_dog.legs_angle_calculation([[0, 80], [0, 40], [30, 0], [30, 75]])

my_dog.do_action("stand", speed=80)
my_dog.wait_all_done()


def pee():
    pee_side = False
    while True:
        my_dog.legs_move([stand], speed=70)
        my_dog.wait_all_done()
        time.sleep(1.5)
        if pee_side := not pee_side:
            my_dog.legs_move([left_pipi], speed=50)
        else:
            my_dog.legs_move([right_pipi], speed=50)
        my_dog.wait_all_done()
        my_dog.speak("pee", 100)
        my_dog.do_action("wag_tail", step_count=5, speed=99)
        time.sleep(5.0)


if __name__ == "__main__":
    try:
        while True:
            pee()
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\033[31mERROR: {e}\033[m")
    finally:
        my_dog.close()
