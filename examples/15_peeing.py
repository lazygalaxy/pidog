#!/usr/bin/env python3
import time
from pidog import Pidog

my_dog = Pidog()

stand = my_dog.legs_angle_calculation([[0, 80], [0, 80], [30, 75], [30, 75]])
left_pipi = my_dog.legs_angle_calculation([[0, 40], [0, 80], [30, 75], [30, 0]])
right_pipi = my_dog.legs_angle_calculation([[0, 80], [0, 40], [30, 0], [30, 75]])

my_dog.do_action("stand", speed=80)
my_dog.wait_all_done()


def pee():
    pee_side = False
    while True:
        # standing position
        my_dog.legs_move([stand], speed=70)
        my_dog.wait_all_done()

        # looking around if anyone is looking!
        time.sleep(1.0)
        head_turn(40)
        my_dog.wait_all_done()
        time.sleep(1.0)
        head_turn(-40)
        my_dog.wait_all_done()
        time.sleep(1.0)
        head_turn(0)
        my_dog.wait_all_done()

        # take a pee
        if pee_side := not pee_side:
            my_dog.legs_move([left_pipi], speed=50)
            head_turn(40,-20)
        else:
            my_dog.legs_move([right_pipi], speed=50)
            head_turn(-40,20)
        my_dog.wait_all_done()
        my_dog.speak("../sounds/peeing.mp3", 100)
        my_dog.do_action("wag_tail", step_count=5, speed=99)
        time.sleep(5.0)


def head_turn(my_dog, x_posi=0, y_posi=0):
    yrp = [0, 0, y_posi]
    head_posi = [x_posi + yrp[0], 0 + yrp[1], 0 + yrp[2]]
    my_dog.head_move(head_posi, speed=92)
    my_dog.wait_all_done()

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
