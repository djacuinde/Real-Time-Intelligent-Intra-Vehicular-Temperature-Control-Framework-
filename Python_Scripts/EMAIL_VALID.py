#CHECKS IF THE EMAIL IS VALID OR NOT
    #IF VALID RETURN TRUE
    #ELSE RETURN FALSE

import re as valid

# Make a regular expression for validating an Email
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
# for custom mails use: '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

def check(email):
    # Check for email validation
    if(valid.search(regex,email)):  
        return True
    else:  
        return False
    
