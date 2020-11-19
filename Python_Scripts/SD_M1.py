
#Functions:
def resetVars():
    startTime = 0.0
    endTime = 0.0
    elapseTime = 0.0
    detectIterations = 0
    DOG_Stat = 0
    CAT_Stat = 0
    PERSON_Stat = 0
    confidenceThreshold = 70.0

#pip3 install adafruit-circuitpython-dht
#sudo apt-get install libgpiod2
def readDTH():
    temperature = dht_device.temperature
    now = datetime.now()    
    current_time = now.strftime ("%I:%M:%S %p") #output time to format HH:MM:SS AM/PM
    print ("Time =", current_time)
    print("Temp = {0:0.1f} C ".format(temperature))
    return temperature

####################################Libraries########################################
# Movidius NCS2
# from openvino.inference_engine import IENetwork 
# from openvino.inference_engine import IEPlugin
# 
# #Object Detection Model
# from intel.yoloparams import TinyYOLOV3Params
# from intel.tinyyolo import TinyYOLOv3
# 
# #Video
# from imutils.video import VideoStream
# from pyimagesearch.utils import Conf
# from imutils.video import FPS
# 
# import numpy as np
# import argparse #Command Line interface
# import imutils #Video
# import cv2 #OpenCV
#import os
import board
import adafruit_dht
import time
from datetime import datetime

#######################################SETUP########################################
#Time

print("Initializing Parameters")
startTime = 0.0
endTime = 0.0
elapseTime = 0.0
setTime = 10.0 #seconds (30sec)

#Detection
detectIterations = 0
DOG_Stat = 0
CAT_Stat = 0
PERSON_Stat = 0
confidenceThreshold = .70

#Sensor
#DTH22 with data_pin on GPIO4 on Pi
dht_device = adafruit_dht.DHT22(board.D4, use_pulseio=False)

#Flag
detectResult = False 

print("Runnig Code Now!")

#Start of Code:
while(detectResult == False):

    startTime = time.perf_counter()
    while(elapseTime < setTime):
        #Detect
        
        DOG_Stat = 500
        CAT_Stat = 0
        PERSON_Stat = 20

        detectIterations = detectIterations + 1
        endTime = time.perf_counter()
        elapseTime = endTime - startTime #seconds
        print(elapseTime)
        
    print("TIME reached!")
    
    #calculate confidence level
    print("Calculating OD Stats")
    IterationPercentage = elapseTime / detectIterations
    print(IterationPercentage)
    
    DOG_Final= DOG_Stat * IterationPercentage
    print(DOG_Final)
    
    CAT_Final= CAT_Stat * IterationPercentage
    print(CAT_Final)
    
    PERSON_Final= PERSON_Stat * IterationPercentage
    print(PERSON_Final)

    if(PERSON_Final > confidenceThreshold ):
        #do nothing
        detectResult = False
        print("detectResult = False")

    elif((DOG_Final > confidenceThreshold or CAT_Final > confidenceThreshold) and PERSON_Final < confidenceThreshold ):
        #pet is detected
        detectResult = True
        print("detectResult = True")
    else :
        detectResult = False
        print("detectResult = False")
        
if (detectResult == True):
    #Close resources
    print("Reading TEMP")
    Current_Temp = readDTH()
    print(Current_Temp)


