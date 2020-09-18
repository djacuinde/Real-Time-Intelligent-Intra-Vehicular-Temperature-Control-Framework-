import Adafruit_DHT
import time
from datetime import datetime

DHT_SENSOR = Adafruit_DHT.DHT22 #Type of sensor (DTH11 or DTH22)
DHT_PIN = 4 #GPIO Pin Number

target_temp = 72.0 #Fahrenheit
Kp = 1 #proportional constant 
Ki = 1 #intregal constant

def getTime():
    now = datetime.now()
    current_time = now.strftime ("%I:%M:%S %p")
    print ("Time =", current_time)

def reset_PIVars():
    current_temp = 0
    error = 0
    intregal = 0

def readDTH():
    humidity, temp_C = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        getTime()
        temp_F = 9/5.0*temp_C+32
        print("Temp = {0:0.1f} F ; Humidity = {1:0.1f}%".format(temp_F, humidity))
        return temp_F
    else:
        print("Cannot read sensor or lost connection! Please Wait! ");
        return 0
    time.sleep(1);


def temp_PIController():
    current_temp = readDTH()
    if current_temp is 0:
        temp_PIController()
    else:
        error = target_temp - current_temp
        integral = intregal + error
        pwm = (Kp*error) + (Ki*intregal)

        if (pwm > 0)
            print ("Turn on AC")
        if (pwm < 0)
            print ("Turn off AC")
    
if __name__ == '__main__':
    reset_PIVars()
    temp_PIController()




