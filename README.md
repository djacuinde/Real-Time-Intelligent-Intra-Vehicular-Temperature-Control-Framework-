# Saving_Lifes_with_ML_-_OBDII


The  project is a real-time camera-based  monitoring system, capable of identifying an object leftunattendedin a vehicle setting and take an appropriate action. The project has an initial focus on commonhousehold pets, specifically dogs, and cats.This decision was made to limit the scope of the project withthe idea that after successful implementation for pets, the project could be expanded to include childrenas  well. For the  identifying  portion of the project, machine  learning will be used. This  project will use one of You Only Look Once (YOLO) real-time object detection models, specifically YOLOv3_Tiny. As for the data set for the object detection model, Common Objects in Context (COCO) will be used and later modified to necessary needs. For the reaction portion of the project, Davy Zide Qian’s methods of preventing children from being left in a car will be used.  Qian’s method uses WIFI or Bluetooth connectivity to send a  notification to a registered email address about the pet left inside the vehicle.  In addition to this notification, control of the vehicle’s heating and air conditioning system will be done via the On-Board Diagnostics (OBD-II) port to bring the temperature  within  the set threshold. In order to monitor the vehicle’s ambient temperature, the system has a DHT11  temperature  sensor  integrated. The entire system will be running on a single Raspberry Pi 4B 4GB and Python programming language. In order to increase the computing speed, an Intel Neural Computer Stick 2 will be used to accelerate the machine learning process.

Project Developers:

Daniel Jacuinde-Alvarez (CSU, Fresno)
James Dols (CSU, Fresno)
