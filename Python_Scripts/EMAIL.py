import smtplib
from cryptography.fernet import Fernet

cs = Fernet(b'BVeJdI_IyCFvwedgYx7QeCUVFiWC-cZW7pcJWpD6yo8=') #key
ct = b'gAAAAABfDhfuj5exwWLvrXrIZWEwXsafl58DedStR7mTw_fZKdMp2jzfMQ7iY2G03jg-vXEpmKkRHGW_flv6FngfRX--o7-6Fg==' #cipher password

SMTP_SERVER = 'smtp.gmail.com' #Email Server 
SMTP_PORT = 587 #Server Port 
GMAIL_USERNAME = 'savinglife2020fresnostate@gmail.com' #gmail account

class Emailer:
    def sendmail(self, recipient, subject, content):
         
        #Create Headers
        headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
                   "MIME-Version: 1.0", "Content-Type: text/html"]
        headers = "\r\n".join(headers)
 
        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
 
        #Login to Gmail
        session.login(GMAIL_USERNAME, bytes(cs.decrypt(ct)).decode("utf-8"))
 
        #Send Email & Exit
        session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
        session.quit
 
sender = Emailer()

sendTo = 'd.jacuinde96@gmail.com' #user account
emailSubject = "PVH Prevention Service"
emailContent = "There is an unattended PET or CHILD is your vehicle!"

#Sends an email
sender.sendmail(sendTo, emailSubject, emailContent)  
