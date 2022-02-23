from pynput import keyboard
rotating = False
moving = False
def on_press(key):
    global rotating
    global moving
    if key.char == 'q' and not rotating:
        print('45')
        rotating = True
    if key.char == 'z' and not moving:
        print('forward')
        moving = True
    if key.char == 's' and not moving:
        print('backward')
        moving = True
    if key.char == 'd' and not rotating:
        print('-45')
        rotating = True

def on_release(key):
    global moving
    global rotating
    if key.char == 'q' and rotating:
        print('0')
        rotating = False
    if key.char == 'z' and moving:
        print('stop')
        moving = False
    if key.char == 's' and moving:
        print('stop')
        moving = False
    if key.char == 'd' and rotating:
        print('0')
        rotating=False
    if key.char == 'n':
        exit()

with keyboard.Listener(
        on_press=on_press, on_release=on_release) as listener:
    listener.join()

