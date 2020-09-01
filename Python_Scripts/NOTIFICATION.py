#enable google less secure app setting by https://www.google.com/settings/security/lesssecureapps

import smtplib
from cryptography.fernet import Fernet

#EMAIL_PASSWORD key
cs = Fernet(b'BVeJdI_IyCFvwedgYx7QeCUVFiWC-cZW7pcJWpD6yo8=')
#EMAIL_PASSWORD cipher password
ct = b'gAAAAABfDhfuj5exwWLvrXrIZWEwXsafl58DedStR7mTw_fZKdMp2jzfMQ7iY2G03jg-vXEpmKkRHGW_flv6FngfRX--o7-6Fg==' 

carriers ={
    'att' : '@txt.att.net',
    'tmobile' : '@tmomail.net',
    'verizon': '@vtext.com',
    'sprint' : '@page.nextel.com'  #'@messaging.sprintpcs.com'
    }

SMTP_SERVER = 'smtp.gmail.com' #Email Server 
SMTP_PORT = 587 #Server Port 
GMAIL_USERNAME = 'savinglife2020fresnostate@gmail.com' #gmail account of SENDER
subject = "PVH Prevention Service"
content = "There is an unattended PET or CHILD is your vehicle!"

#PHONE_NUM = '5597045940{}'.format (carriers['att']) #Pet's owner phone number ####encrypt number?####
PHONE_NUM = '';
recipient = '';


class Notification:
    def sendNotification():
        
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
        #session.login(GMAIL_USERNAME, bytes(cs.decrypt(ct)).decode("utf-8"))
        ##session.login('d.jacuinde96@gmail.com', 'PASSWORDHERE')
 
        #Send Email & SMS then Exit
        session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content) #email
        session.sendmail(GMAIL_USERNAME, PHONE_NUM, content)#sms 
        session.quit
        
    def SetEMAIL(email):
        recipient = email
    
    def SetPHONE (phoneNumber, carrierType):
        PHONE_NUM = str(phoneNumber{}).format(carriers[str(carrierType)])
 

 