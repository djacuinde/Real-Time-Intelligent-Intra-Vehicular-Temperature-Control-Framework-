#needs to be in the same directory or specific where

from NOTIFICATION import *
from EMAIL_VALID import *

#Prompt for owner's email 
E = input('Owner EMAIL: ')

checkFLAG = check(E)

if checkFLAG == False:
    print("INVALID!")
else :
    print("OK")
    #Prompt for owner's email 
    N = input('Owner NUMBER: ')
    C = input('Carrier Type: a) att b) tmobile c) verzion d) sprint e) other')
    
    s =Notification
    s.sendNotification(E, N, C)
    #g.sendNotification()
    print ("CHECK")

