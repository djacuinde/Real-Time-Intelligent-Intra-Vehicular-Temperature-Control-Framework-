#sudo pip3 install Adafruit_DHT

import Adafruit_DHT
import time

DHT_SENSOR = Adafruit_DHT.DHT11 #Type of sensor (DTH11 or DTH22)
DHT_PIN = 4 #GPIO Pin Number
Degree = 'F' #F = Fahrenheit, C = Celsius 

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        if Degree is 'F':
            print("Temp={0:0.1f}F Humidity={1:0.1f}%".format(9/5.0*temperature+32, humidity))
        if Degree is 'C':
            print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Sensor failure. Check wiring.");
    time.sleep(3);#delay of 3
