#enable google less secure app setting by https://www.google.com/settings/security/lesssecureapps

import smtplib
from cryptography.fernet import Fernet

#EMAIL_PASSWORD key
cs = Fernet(b'BVeJdI_IyCFvwedgYx7QeCUVFiWC-cZW7pcJWpD6yo8=')
#EMAIL_PASSWORD cipher password
ct = b'gAAAAABfDhfuj5exwWLvrXrIZWEwXsafl58DedStR7mTw_fZKdMp2jzfMQ7iY2G03jg-vXEpmKkRHGW_flv6FngfRX--o7-6Fg==' 

carriers ={
    'a' or 'att' : '@txt.att.net',
    'b' or 'tmobile' : '@tmomail.net',
    'c' or 'verizon': '@vtext.com',
    'd' or 'sprint' : '@page.nextel.com'  #'@messaging.sprintpcs.com'
    }

SMTP_SERVER = 'smtp.gmail.com' #Email Server 
SMTP_PORT = 587 #Server Port 
GMAIL_USERNAME = 'savinglife2020fresnostate@gmail.com' #gmail account of SENDER
SUBJECT = "PVH Prevention Service"
MESSAGE = "There is an unattended PET or CHILD is your vehicle!"

#PHONE_NUM = '5597045940{}'.format (carriers['att']) #Pet's owner phone number ####encrypt number?####
PHONE_NUM = 'DAFAULT';#?
RECIPIENT = 'DEFAULT';


class Notification:
    def sendNotification(RECIPIENT, phoneNumber, carrierType):
        if RECIPIENT != 'DEFAULT':
        
            #Create Headers
            headers = ["From: " + GMAIL_USERNAME, "Subject: " + SUBJECT, "To: " + RECIPIENT ,
                       "MIME-Version: 1.0", "Content-Type: text/html"]
            headers = "\r\n".join(headers)
     
            #Connect to Gmail Server
            session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            session.ehlo()
            session.starttls()
            session.ehlo()
            
            #Login to Gmail
            #session.login(GMAIL_USERNAME, bytes(cs.decrypt(ct)).decode("utf-8"))
            session.login('d.jacuinde96@gmail.com', 'Greenship_582.')
     
            #Send Email & SMS then Exit
            session.sendmail(GMAIL_USERNAME, RECIPIENT , headers + "\r\n\r\n" + MESSAGE) #email
            
            PHONE_NUM = phoneNumber + '{}'.format(carriers[carrierType]) 
            if PHONE_NUM != 'DEFAULT' : 
                session.sendmail(GMAIL_USERNAME, PHONE_NUM, MESSAGE)#sms
                
            session.quit
        
 

 