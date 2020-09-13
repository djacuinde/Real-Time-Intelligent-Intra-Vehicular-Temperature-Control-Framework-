
#sudo pip3 install Adafruit_DHT

import Adafruit_DHT
import time
from datetime import datetime

DHT_SENSOR = Adafruit_DHT.DHT22 #Type of sensor (DTH11 or DTH22)
DHT_PIN = 4 #GPIO Pin Number

def readDTH(Degree):
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        now = datetime.now()
        current_time = now.strftime ("%I:%M:%S %p")
        print ("Time =", current_time)
        if Degree is 'F':
            print("Temp = {0:0.1f} F ; Humidity = {1:0.1f}%".format(9/5.0*temperature+32, humidity))
        if Degree is 'C':
            print("Temp = {0:0.1f} C ; Humidity = {1:0.1f}%".format(temperature, humidity))
    else:
        print("Cannot read sensor or lost connection !");
    time.sleep(1);
    
if __name__ == '__main__':
    readDTH('F')
