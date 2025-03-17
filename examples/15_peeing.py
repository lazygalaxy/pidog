#!/usr/bin/env python3
import traceback
import time
from pidog import Pidog
from preset_actions import *

my_dog = Pidog()

stand = my_dog.legs_angle_calculation([[0, 80], [0, 80], [30, 75], [30, 75]])

def pee():
    pee_side = False
    while True:
        # standing position with head staright
        body_reset(my_dog)
        peeing(my_dog, pee_side := not pee_side)

def body_reset(my_dog: Pidog):
    head_turn(my_dog)
    my_dog.legs_move([stand], immediately=False, speed=70)
    my_dog.wait_all_done()
    time.sleep(1.0)

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
