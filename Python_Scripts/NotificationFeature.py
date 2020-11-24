#enable google less secure app setting by https://www.google.com/settings/security/lesssecureapps

import smtplib
from cryptography.fernet import Fernet

#EMAIL_PASSWORD key
ck = Fernet(b'FH0uzJ2Yl47lh1xYgcMBchLMbOcLg9gNPepDpOLOmgw=')
#EMAIL_PASSWORD cipher password
ct = b'gAAAAABfqgEZh_XKJgYrF2NeHPYkNyFSgRHbC8c6M94G7hNP9f1aoH7MHqDvZcdImBQxF6PkY36pAXy1Jwy2sOe_hUG9g8DyQw=='

#SMS ending
carriers ={
    'att' : '@txt.att.net',
    'tmobile' : '@tmomail.net',
    'verizon': '@vtext.com',
    'sprint' : '@page.nextel.com'  #'@messaging.sprintpcs.com'
    }

SMTP_SERVER = 'smtp.gmail.com' #Email Server 
SMTP_PORT = 587 #Server Port 
GMAIL_USERNAME = 'savinglife2020fresnostate@gmail.com' #gmail account of SENDER
SUBJECT = 'PVH Prevention Service'
MESSAGE = 'There is an unattended PET is your vehicle!'


class Notification:
    def sendNotification(RECIPIENT, phoneNumber, carrierType):
        
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
            session.login(GMAIL_USERNAME, bytes(ck.decrypt(ct)).decode("utf-8"))
            #session.login(GMAIL_USERNAME, PASSWORD)
            #Send Email & SMS then Exit
            session.sendmail(GMAIL_USERNAME, RECIPIENT , headers + "\r\n\r\n" + MESSAGE) #email
            PHONE_NUM = phoneNumber + '{}'.format(carriers[carrierType])  
            session.sendmail(GMAIL_USERNAME, PHONE_NUM, MESSAGE)#sms 
            session.quit
            
if __name__ == '__main__':
    N = Notification
    N.sendNotification('djacuinde96@gmail.com', '5597045940', 'att')
