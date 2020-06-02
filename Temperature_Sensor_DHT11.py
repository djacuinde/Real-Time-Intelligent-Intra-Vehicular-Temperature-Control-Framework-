
# git clone https://github.com/adafruit/Adafruit_Python_DHT.git
# cd Adafruit_Python_DHT
# sudo apt-get install build-essential python-dev
# sudo python setup.py install

import sys
import Adafruit_DHT

DHT11_temperature = 0.0
DHT11_humidity = 0.0

while True:
    DHT11_humidity, DHT11_temperature = Adafruit_DHT.read_retry (11,4) #(sensor, pin)
    CurrentTemp = Get_Temperature("F", DHT11_temperature)
    print 'Temperature: {0:0.1f} C Humidity: {1:0.1f} %'.format(CurrentTemp, DHT11_humidity)

# temp  = F for Fahrenheit
# temp  = C for Celsius
def Get_Temperature(temp, DHT11_temperature)
    if temp = "F"
        temperature = 9/5.0 * DHT11_temperature + 32
    else if temp = "C"
        temperature = 5.0/9 * (DHT11_temperature - 32)
    return  temperature



#sudo pip3 install Adafruit_DHT

import Adafruit_DHT
import time
 
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
 
while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Sensor failure. Check wiring.");
    time.sleep(3);
