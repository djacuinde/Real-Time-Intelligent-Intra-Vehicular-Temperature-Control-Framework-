#use custom Adafruit_DHT from https://github.com/djacuinde96/Adafruit_Python_DHT.git

import Adafruit_DHT
from datetime import datetime

TempC = 0.0

def readTemp():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)

    now = datetime.now()    
    current_time = now.strftime ("%I:%M:%S %p")
    print ("Time =", current_time)
    if humidity is not None and temperature is not None:
        TempC = '{0:0.1f}*C '.format(temperature)
        print('Temperature = ', TempC)
        return TempC
    else:
        print('Failed to get reading. Try again!')
        return 0

if __name__ == '__main__':
    Temp = readTemp()
    print(Temp)
