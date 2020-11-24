#sudo pip3 install Adafruit_DHT

import board
import adafruit_dht
import time
from datetime import datetime

#DTH22 with data_pin on GPIO4 on Pi
dht_device = adafruit_dht.DHT22(board.D4, use_pulseio=False)

def readDTH():
    temperature = dht_device.temperature
    now = datetime.now()    
    current_time = now.strftime ("%I:%M:%S %p") #output time to format HH:MM:SS AM/PM
    print ("Time =", current_time)
    print("Temp = {0:0.1f} C ".format(temperature))
    return temperature
    
if __name__ == '__main__':
    Temp = readDTH()
    print(Temp)
