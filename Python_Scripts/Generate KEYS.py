from cryptography.fernet import Fernet

#Message to encrypt
string = "passwordHERE"
print("The message is :" , string)

#generate key 
key = Fernet.generate_key()
print("The key is:" , key)

#encode the message to bytes then encrypt the message "
cipher_suite = Fernet(key)
cipher_text = cipher_suite.encrypt(bytes(string, 'utf-8'))
print ("The encypted message is:" ,cipher_text)

#decrypt cipher text and decode the message to plain text
unciphered_text = (cipher_suite.decrypt(cipher_text))
print ("The decrypted message is:", bytes(unciphered_text).decode("utf-8"))