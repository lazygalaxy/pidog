#!/usr/bin/env python3
import traceback
import time
from pidog import Pidog

my_dog = Pidog()

stand = my_dog.legs_angle_calculation([[0, 80], [0, 80], [30, 75], [30, 75]])
left_pipi = my_dog.legs_angle_calculation([[0, 40], [0, 80], [30, 75], [30, 0]])
right_pipi = my_dog.legs_angle_calculation([[0, 80], [0, 40], [30, 0], [30, 75]])


def pee():
    pee_side = False
    while True:
        # standing position with head staright
        body_reset(my_dog)

        # looking around if anyone is looking!
        head_turn(my_dog, 1.0, 40)
        head_turn(my_dog, 1.0, -40)
        head_turn(my_dog, 1.0)

        # take a pee, switch the side
        if pee_side := not pee_side:
            head_turn(my_dog, 0.0, -40, -40)
            my_dog.legs_move([left_pipi], speed=50)

        else:
            head_turn(my_dog, 0.0, 40, -40)
            my_dog.legs_move([right_pipi], speed=50)
        my_dog.speak("../sounds/peeing.mp3", 100)
        my_dog.do_action("wag_tail", step_count=5, speed=99)
        # pee will last 5 seconds
        time.sleep(5.0)


def body_reset(my_dog: Pidog):
    head_turn(my_dog)
    my_dog.legs_move([stand], immediately=False, speed=70)
    my_dog.wait_all_done()
    time.sleep(1.0)


def head_turn(my_dog: Pidog, seconds: float = 0.0, x_posi: int = 0, y_posi: int = 0):
    yrp = [0, 0, y_posi]
    head_posi = [[x_posi + yrp[0], 0 + yrp[1], 0 + yrp[2]]]
    my_dog.head_move(head_posi, immediately=False, speed=92)
    my_dog.wait_all_done()
    time.sleep(seconds)


if __name__ == "__main__":
    try:
        while True:
            pee()
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\033[31mERROR: {e}\033[m")
        stack_trace = traceback.format_exc()
        print(stack_trace)
    finally:
        my_dog.close()
