#import evdev
from evdev import InputDevice, categorize, ecodes

from raspsoft import *
from thread_soft import *
import time

#creates object 'gamepad' to store the data
#you can call it whatever you like
gamepad = InputDevice('/dev/input/event0')

#button code variables (change to suit your device)
up = 307
down = 304 
left = 306
right = 305

#prints out device info at start
print(gamepad)

car = Car()
turnLeft = TurnLeft(135)
turnRight = TurnRight(45)
forward = Forward(80)
backward = Backward(80)

#loop and filter by event code and print the mapped label
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.value == 1:
            if event.code == up:
                print("Up")
                car.add_state(forward)
                time.sleep(1)
                car.remove_state(forward)
                print("up")
                time.sleep(1)
            elif event.code == down:
                print("Down")
                car.add_state(backward)
                time.sleep(1)
                car.remove_state(backward)
                print("down")
                time.sleep(1)
            elif event.code == left:
                print("Left")
                car.add_state(turnLeft)
                time.sleep(1)
                car.remove_state(turnLeft)
                print("left")
                time.sleep(1)
            elif event.code == right:
                print("Right")
                car.add_state(turnRight)
                time.sleep(1)
                car.remove_state(turnRight)
                print("right")
                time.sleep(1)
