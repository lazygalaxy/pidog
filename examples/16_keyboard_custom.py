#!/usr/bin/env python3
import time
from pidog import Pidog
from preset_actions import *
import sys
import tty
import termios

# init pidog
# ======================================
my_dog = Pidog()
time.sleep(0.5)

# global variables
# ======================================
SIT_HEAD_PITCH = -40
STAND_HEAD_PITCH = 0
STATUS_STAND = 0
STATUS_SIT = 1
STATUS_LIE = 2
HEAD_SPEED = 80
HEAD_ANGLE = 20

head_yrp = [0, 0, 0]
head_pitch_init = 0
command = None
current_status = STATUS_LIE

last_key = None

# KEYS and OPERATIONS:dict
# ======================================
KEYS = {
    "1": {  # keyname
        "pos": [0, 0], # ypos, xpos
        "tip": ["Doze", "Off"],
        "operation": "doze off",
    },
    "2": {
        "pos": [0, 10],
        "tip": ["Push", "Up"],
        "operation": "push up",
    },
    "3": {
        "pos": [0, 20],
        "tip": ["Howling", ""],
        "operation": "howling",
    },
    "4": {
        "pos": [0, 30],
        "tip": ["Body", "Twist"],
        "operation": "twist body",
    },
    "5": {
        "pos": [0, 40],
        "tip": ["Scratch", ""],
        "operation": "scratch",
    },
    "6": {
        "pos": [0, 50],
        "tip": ["", ""],
        "operation": None,
    },
    "7": {
        "pos": [0, 60],
        "tip": ["", ""],
        "operation": None,
    },
    "8": {
        "pos": [0, 70],
        "tip": ["", ""],
        "operation": None,
    },
    "9": {
        "pos": [0, 80],
        "tip": ["", ""],
        "operation": None,
    },
    "0": {
        "pos": [0, 90],
        "tip": ["", ""],
        "operation": None,
    },
    # #################################
    "q": {
        "pos": [5, 5],
        "tip": ["Bark", ""],
        "operation": "bark",
    },
    "w": {
        "pos": [5, 15],
        "tip": ["Forward", ""],
        "operation": "forward",
    },
    "W": {
        "pos": [5, 15],
        "tip_upper": "Trot",
        "operation": "trot",
    },
    "e": {
        "pos": [5, 25],
        "tip": ["Pant", ""],
        "operation": "pant",
    },
    "r": {
        "pos": [5, 35],
        "tip": ["Wag", "Tail"],
        "operation": "wag tail",
    },
    "t": {
        "pos": [5, 45],
        "tip": ["Hand", "Shake"],
        "operation": "handshake",
    },
    "y": {
        "pos": [5, 55],
        "tip": ["", ""],
        "operation": None,
    },
    "u": {
        "pos": [5, 65],
        "tip": ["Head", "Roll"],
        "operation": None,
    },
    "U": {
        "pos": [5, 65],
        "tip_upper": "x2",
        "operation": None,
    },
    "i": {
        "pos": [5, 75],
        "tip": ["Head", "Pitch"],
        "operation": None,
    },
    "I": {
        "pos": [5, 75],
        "tip_upper": "x2",
        "operation": None,
    },
    "o": {
        "pos": [5, 85],
        "tip": ["Head", "Roll"],
        "operation": None,
    },
    "O": {
        "pos": [5, 85],
        "tip_upper": "x2",
        "operation": None,
    },
    "p": {
        "pos": [5, 95],
        "tip": ["", ""],
        "operation": None,
    },
    "P": {
        "pos": [5, 95],
        "tip_upper": " ",
        "operation": None,
    },
    ####################
    "a": {
        "pos": [10, 9],
        "tip": ["Turn", "Left"],
        "operation": "turn left",
    },
    "s": {
        "pos": [10, 19],
        "tip": ["Backward", ""],
        "operation": "backward",
    },
    "d": {
        "pos": [10, 29],
        "tip": ["Turn", "Right"],
        "operation": "turn right",
    },
    "f": {
        "pos": [10, 39],
        "tip": ["Shake", "Head"],
        "operation": "shake head",
    },
    "g": {
        "pos": [10, 49],
        "tip": ["High", "Five"],
        "operation": "high five",
    },
    "h": {
        "pos": [10, 59],
        "tip": ["", ""],
        "operation": None,
    },
    "j": {
        "pos": [10, 69],
        "tip": ["Head", "Yaw"],
        "operation": None,
    },
    "J": {
        "pos": [10, 69],
        "tip_upper": "x2",
        "operation": None,
    },
    "k": {
        "pos": [10, 79],
        "tip": ["Head", "Pitch"],
        "operation": None,
    },
    "K": {
        "pos": [10, 79],
        "tip_upper": "x2",
        "operation": None,
    },
    "l": {
        "pos": [10, 89],
        "tip": ["Head", "Yaw"],
        "operation": None,
    },
    "L": {
        "pos": [10, 89],
        "tip_upper": "x2",
        "operation": None,
    },
    #############
    "z": {
        "pos": [15, 12],
        "tip": ["Lie", ""],
        "operation": "lie",
    },
    "x": {
        "pos": [15, 22],
        "tip": ["Stand", ""],
        "operation": "stand",
    },
    "c": {
        "pos": [15, 32],
        "tip": ["Sit", ""],
        "operation": "sit",
    },
    "v": {
        "pos": [15, 42],
        "tip": ["Stretch", ""],
        "operation": "stretch",
    },
    "b": {
        "pos": [15, 52],
        "tip": ["", ""],
        "operation": None,
    },
    "n": {
        "pos": [15, 62],
        "tip": ["", ""],
        "operation": None,
    },
    "m": {
        "pos": [15, 72],
        "tip": ["Head", "Reset"],
        "operation": None,
    },
}

OPERATIONS = {
    "forward": {
        "function": lambda: my_dog.do_action('forward', speed=98),
        "status": STATUS_STAND,
        "head_pitch": STAND_HEAD_PITCH,
    },
    "backward": {
        "function": lambda: my_dog.do_action('backward', speed=98),
        "status": STATUS_STAND,
        "head_pitch": STAND_HEAD_PITCH,
    },
    "turn left": {
        "function": lambda: my_dog.do_action('turn_left', speed=98),
        "status": STATUS_STAND,
        "head_pitch": STAND_HEAD_PITCH,
    },
    "turn right": {
        "function": lambda: my_dog.do_action('turn_right', speed=98),
        "status": STATUS_STAND,
        "head_pitch": STAND_HEAD_PITCH,
    },
    "trot": {
        "function": lambda: my_dog.do_action('trot', speed=98),
        "status": STATUS_STAND,
        "head_pitch": STAND_HEAD_PITCH,
    },
    "stop": {
    },
    "lie": {
        "function": lambda: my_dog.do_action('lie', speed=70),
        "head_pitch": STAND_HEAD_PITCH,
        "status": STATUS_LIE,
    },
    "stand": {
        "function": lambda: my_dog.do_action('stand', speed=70),
        "head_pitch": STAND_HEAD_PITCH,
        "status": STATUS_STAND,
    },
    "sit": {
        "function": lambda: my_dog.do_action('sit', speed=70),
        "head_pitch": SIT_HEAD_PITCH,
        "status": STATUS_SIT,
    },
    "bark": {
        "function": lambda: bark(my_dog, head_yrp, pitch_comp=head_pitch_init),
    },
    "bark harder": {
        "function": lambda: bark_action(my_dog, head_yrp, 'single_bark_1'),
    },
    "pant": {
        "function": lambda: pant(my_dog, head_yrp, pitch_comp=head_pitch_init),
    },
    "wag tail": {
        "function": lambda: my_dog.do_action('wag_tail', speed=100),
        "after": "wag tail",
    },
    "shake head": {
        "function": lambda: shake_head(my_dog,[ head_yrp[0], head_yrp[1], head_yrp[2]+head_pitch_init]),
    },
    "stretch": {
        "function": lambda: my_dog.do_action('stretch', speed=80),
        # "after": "stand",
        "status": STATUS_STAND,
    },
    "doze off": {
        "function": lambda: my_dog.do_action('doze_off', speed=95),
        "after": "doze off",
        "status": STATUS_LIE,
    },
    "push up": {
        "function": lambda: push_up(my_dog),
        "status": STATUS_STAND,
    },
    "howling": {
        "function": lambda: howling(my_dog),
        "after": "sit",
        "status": STATUS_SIT,
    },
    "twist body": {
        "function": lambda: body_twisting(my_dog),
        "before": "stretch",
        "after": "sit",
        "status": STATUS_STAND,
    },
    "scratch": {
        "function": lambda: scratch(my_dog),
        "after": "sit",
        "head_pitch": SIT_HEAD_PITCH,
        "status": STATUS_SIT,
    },
    "handshake": {
        "function": lambda: hand_shake(my_dog),
        "after": "sit",
        "head_pitch": SIT_HEAD_PITCH,
        "status": STATUS_SIT,
    },
    "high five": {
        "function": lambda: high_five(my_dog),
        "after": "sit",
        "head_pitch": SIT_HEAD_PITCH,
        "status": STATUS_SIT,
    },
}

# set_head_pitch_init(pitch)
# ======================================
def set_head_pitch_init(pitch):
    global head_pitch_init
    head_pitch_init = pitch
    my_dog.head_move([head_yrp], pitch_comp=pitch,
                     immediately=True, speed=HEAD_SPEED)

# change_status(status)
# ======================================
def change_status(status):
    global current_status
    current_status = status
    if status == STATUS_STAND:
        set_head_pitch_init(STAND_HEAD_PITCH)
        my_dog.do_action('stand', speed=70)
    elif status == STATUS_SIT:
        set_head_pitch_init(SIT_HEAD_PITCH)
        my_dog.do_action('sit', speed=70)
    elif status == STATUS_LIE:
        set_head_pitch_init(STAND_HEAD_PITCH)
        my_dog.do_action('lie', speed=70)
    my_dog.wait_all_done()

#
# ======================================
def run_operation(key):
    global command, head_pitch_init, head_yrp
    if not my_dog.is_legs_done() or not my_dog.is_head_done():
        return

    key_data = None
    operation = None
    # before = None
    # after = None
    if key not in KEYS.keys():
        sleep(0.2)
        return
    else:
        key_data = KEYS[key]

    # head control
    if key in ('uiojklmUIOJKL'):
        # Head Pitch
        if key == 'i':
            head_yrp[2] = HEAD_ANGLE
        elif key == 'I':
            head_yrp[2] = HEAD_ANGLE * 2
        elif key == 'k':
            head_yrp[2] = -HEAD_ANGLE
        elif key == 'K':
            head_yrp[2] = -HEAD_ANGLE * 2
        # Head Yaw
        elif key == 'j':
            head_yrp[0] = HEAD_ANGLE
        elif key == 'J':
            head_yrp[0] = HEAD_ANGLE * 2
        elif key == 'l':
            head_yrp[0] = -HEAD_ANGLE
        elif key == 'L':
            head_yrp[0] = -HEAD_ANGLE * 2
        # Head Roll
        elif key == 'u':
            head_yrp[1] = -HEAD_ANGLE
        elif key == 'U':
            head_yrp[1] = -HEAD_ANGLE * 2
        elif key == 'o':
            head_yrp[1] = HEAD_ANGLE
        elif key == 'O':
            head_yrp[1] = HEAD_ANGLE * 2
            # Head Reset
        elif key == 'm':
            head_yrp = [0, 0, 0]
        my_dog.head_move([head_yrp], pitch_comp=head_pitch_init,
                            immediately=True, speed=HEAD_SPEED)
        return
    # actions
    if "operation" in key_data and key_data["operation"] != None:
        if key_data["operation"] in OPERATIONS:
            operation = OPERATIONS[key_data["operation"]]
        else:
            return
        # status
        if "status" in operation and operation["status"] != None:
            if current_status != operation["status"]:
                change_status(operation["status"])
        # before
        if "before" in operation and operation["before"] != None:
            before = operation["before"]
            if before in OPERATIONS and OPERATIONS[before]["function"] != None:
                OPERATIONS[before]["function"]() # run before function
        # function
        if "function" in operation and operation["function"] != None:
            operation["function"]() # run function function
        # after
        if "after" in operation and operation["after"] != None:
            after = operation["after"]
            if after in OPERATIONS and OPERATIONS[after]["function"] != None:
                OPERATIONS[after]["function"]() # run after function


def get_key():
    """Reads a single key press and returns its integer (ASCII) value."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)  # Set terminal to raw mode (no Enter required)
        key = sys.stdin.read(1)  # Read one character
        return ord(key)  # Convert character to ASCII integer
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # Restore settings


def main():
    global last_key

    while True:
        key = get_key()
        if key is not None and key > 32 and key < 127:
            key = chr(key)
            if key in KEYS:
                if last_key != key:
                    my_dog.body_stop()
                    my_dog.rgb_strip.close()
                # stdscr.move(curses_utils.PAD_Y+1, 0)
                # stdscr.refresh()
                run_operation(key)
                last_key = key
                sleep(0.01)
        else:
            if last_key != None and my_dog.is_all_done():
                # stdscr.move(curses_utils.PAD_Y+1, 0)
                # stdscr.refresh()
                last_key = None

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\033[31mERROR: {e}\033[m")
    finally:
        my_dog.close()
