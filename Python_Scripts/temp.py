##################################START OF FILE#####################################

#Run the command below using Command Line using video example
# $ python detect_realtime_tinyyolo_ncs.py --conf config/config.json --input videos/test_video.mp4

#Run the command below using Command Line using pi Camera
# $ python detect_realtime_tinyyolo_ncs.py --conf config/config.json 

# Script was developed by Adrian Rosebrock
# Modified by Daniel Jacuinde from CSU, Fresno

####################################Functions########################################

def resetVars():
    startTime = 0.0
    endTime = 0.0
    elapseTime = 0.0
    detectIterations = 0
    DOG_Stat = 0
    CAT_Stat = 0
    PERSON_Stat = 0


def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)


def on_resubscribe_complete(resubscribe_future):
        resubscribe_results = resubscribe_future.result()
        print("Resubscribe results: {}".format(resubscribe_results))

        for topic, qos in resubscribe_results['topics']:
            if qos is None:
                sys.exit("Server rejected resubscribe to topic: {}".format(topic))


# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, **kwargs):
    #global current_temp
    global finish
    print("Received message from topic '{}': {}".format(topic, payload))
    topic_parsed = False
    if "/" in topic:
        parsed_topic = topic.split("/")
        if len(parsed_topic) == 3:
            # this topic has the correct format
            if (parsed_topic[0] == 'SD_M2') and (parsed_topic[2] == 'details'):
                # this is a topic we care about, so check the 2nd element
                if (parsed_topic[1] == 'recheck'):
                    print("Status: {}".format(payload))
                    #current_temp = float(payload)  ##Convert the received string into a float. 
                    #if current_temp == -999.0:##recieving a payload value of -999.0 will cause the session to disconnect.
                        if (Status == 'Complete')
                            finish = True
                topic_parsed = True            
    if not topic_parsed:
            print("Unrecognized message topic.")
    global received_count
    received_count += 1
    if received_count == incount:
        received_all_event.set()

##Subscription Topic
def subscribe(subscribed_topic):  ##pass in topic name in string format. ex SD_M1/temp/details
    # Subscribe
    print("Subscribing to topic '{}'...".format(subscribed_topic))
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=subscribed_topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)

    subscribe_result = subscribe_future.result()
    print("Subscribed with {}".format(str(subscribe_result['qos'])))

##Publish to a topic
def publish_topic(pub_top_name,pub_top_message):
    global publish_count
    print("Publishing message to topic '{}': {}".format(pub_top_name, pub_top_message))
    mqtt_connection.publish(
        topic=pub_top_name,
        payload=pub_top_message,
        qos=mqtt.QoS.AT_LEAST_ONCE)
    time.sleep(1)
    publish_count += 1 
####################################Libraries########################################

# Movidius NCS2
from openvino.inference_engine import IENetwork 
from openvino.inference_engine import IEPlugin

#Object Detection Model
from intel.yoloparams import TinyYOLOV3Params
from intel.tinyyolo import TinyYOLOv3

#Video
from imutils.video import VideoStream
from pyimagesearch.utils import Conf
from imutils.video import FPS

#Other
import numpy as np
import argparse
import imutils
import time
import cv2
import os

#Temperature 
from DTH import readTemp

##AWS IoT Core
import argparse
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time
from uuid import uuid4

#######################################SETUP########################################
def Object_Detection():
    #Topics
    incoming_topic = 'SD_M2/recheck/details'
    outgoing_topic = 'SD_M1/temp/details'

    ##AWS IoT logging
    #original line: io.init_logging(getattr(io.LogLevel, args.verbosity), 'stderr')
    io.init_logging(getattr(io.LogLevel, io.LogLevel.NoLogs.name), 'stderr')

    ##connect to AWS
    ##connection variables
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    ##Replace the below with necessary value for thing M1 or M2
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint='a3f97mcy639kgs-ats.iot.us-east-2.amazonaws.com',
        cert_filepath="/home/pi/certs/device.pem.crt",
        pri_key_filepath='/home/pi/certs/private.pem.key',
        client_bootstrap=client_bootstrap,
        ca_filepath='/home/pi/certs/Amazon-root-CA-1.pem',
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id="SD_M1-" + str(uuid4()),
        clean_session=False,
        keep_alive_secs=6)
    ##Redefined endpoint and client as local variables##This is not strictly needed except for print statement.    
    endpoint='a3f97mcy639kgs-ats.iot.us-east-2.amazonaws.com'
    client_id="SD_M1-" + str(uuid4())

    print("Connecting to {} with client ID '{}'...".format(endpoint, client_id))

    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected to AWS!")

    subscribe(incoming_topic)


    #Object Detection
    print("Initializing Parameters")
    startTimerTime = 0.0
    endTimerTime = 0.0
    elapseTimerTime = 0.0
    setTimerTime = 10.0 #seconds (30sec)

    #Detection
    detectIterations = 0
    DOG_Stat = 0
    CAT_Stat = 0
    PERSON_Stat = 0
    confidenceTimeThreshold = .70

    #intilize variables AWS
    received_count = 0 
    publish_count = 0
    received_all_event = threading.Event()
    lastsendtime = 0.0
    global finish
    finish = False



    # Command Line Interface #
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conf", required=True,
        help="Path to the input configuration file")
    ap.add_argument("-i", "--input", help="path to the input video file")
    args = vars(ap.parse_args())

    # load the configuration file
    conf = Conf(args["conf"])

    # COCO label and corresponding color preparation #
    # load the COCO class labels that YOLO model was trained on and
    # initialize a list of colors to represent each possible class label
    LABELS = open(conf["labels_path"]).read().strip().split("\n")
    np.random.seed(42)
    COLORS = np.random.uniform(0, 255, size=(len(LABELS), 3))

    # Load tinyYOLOv3 modle onto Movidius NCS2 #
    # initialize the plugin in for specified device
    plugin = IEPlugin(device="MYRIAD")

    # read the IR generated by the Model Optimizer (.xml and .bin files)
    #.xml is YOLO architecture & .bin is the pretrained weights
    print("[INFO] loading models...")
    net = IENetwork(model=conf["xml_path"], weights=conf["bin_path"])

    # prepare inputs
    print("[INFO] preparing inputs...")
    inputBlob = next(iter(net.inputs))

    # set the default batch size as 1 and get the number of input blobs,
    # number of channels, the height, and width of the input blob
    net.batch_size = 1
    (n, c, h, w) = net.inputs[inputBlob].shape

    # /Image input reference for tinyYOLOv3 #
    # if a video path was not supplied, grab a reference to the webcam
    if args["input"] is None:
        print("[INFO] starting video stream...")
        # vs = VideoStream(src=0).start() #USB Camera
        vs = VideoStream(usePiCamera=True).start() #Pi Camera
        time.sleep(2.0)
        # otherwise, grab a reference to the video file
    else:
        print("[INFO] opening image/video file...")
        vs = cv2.VideoCapture(os.path.abspath(args["input"]))
        
    # loading model to the plugin and start the frames per second
    # throughput estimator
    print("[INFO] loading model to the plugin...")
    execNet = plugin.load(network=net, num_requests=1)
    fps = FPS().start()

    ######################################Processing#####################################

    #Detection Flag
    detectResult = False 

    print("[INFO] Runnig Detection...")

    while(detectResult == False):
        
        startTimerTime = time.perf_counter()
        while(elapseTimerTime < setTimerTime):
            
            # grab the next frame and handle VideoCapture or VideoStream
            orig = vs.read()
            orig = orig[1] if args["input"] is not None else orig

            # if we are viewing a video and we did not grab a frame then we
            # have reached the end of the video
            if args["input"] is not None and orig is None:
                break

            # resize original frame to have a maximum width of 500 pixel and
            # input_frame to network size
            orig = imutils.resize(orig, width=500)
            frame = cv2.resize(orig, (w, h))

            # change data layout from HxWxC to CxHxW
            frame = frame.transpose((2, 0, 1))
            frame = frame.reshape((n, c, h, w))

            # start inference and initialize list to collect object detection
            # results
            output = execNet.infer({inputBlob: frame})
            objects = []

            # loop over the output items
            for (layerName, outBlob) in output.items():
                # create an object with required tinyYOLOv3 parameters
                layerParams = TinyYOLOV3Params(net.layers[layerName].params,
                    outBlob.shape[2])

                # parse the output region
                objects += TinyYOLOv3.parse_yolo_region(outBlob,
                    frame.shape[2:], orig.shape[:-1], layerParams,
                    conf["prob_threshold"])

            # loop over each of the objects
            for i in range(len(objects)):
                # check if the confidence of the detected object is zero, if
                # it is, then skip this iteration, indicating that the object
                # should be ignored
                if objects[i]["confidence"] == 0:
                    continue

                # loop over remaining objects[Intersection over Union (IoU)]
                for j in range(i + 1, len(objects)):
                    # check if the IoU of both the objects exceeds a
                    # threshold, if it does, then set the confidence of
                    # that object to zero
                    if TinyYOLOv3.intersection_over_union(objects[i],
                        objects[j]) > conf["iou_threshold"]:
                        objects[j]["confidence"] = 0

            # filter objects by using the probability threshold -- if a an
            # object is below the threshold, ignore it
            objects = [obj for obj in objects if obj['confidence'] >= \
                conf["prob_threshold"]]

        ############################Object Detection Frame & Stats###########################

            # store the height and width of the original frame
            (endY, endX) = orig.shape[:-1]

            # loop through all the remaining objects
            for obj in objects:
                # validate the bounding box of the detected object, ensuring
                # we don't have any invalid bounding boxes
                if obj["xmax"] > endX or obj["ymax"] > endY or obj["xmin"] \
                    < 0 or obj["ymin"] < 0:
                    continue

                # build a label consisting of the predicted class and
                # associated probability
                label = "{}: {:.2f}%".format(LABELS[obj["class_id"]],
                    obj["confidence"] * 100)
                print(label)
                
                tag = LABELS[obj["class_id"]]
                if (tag == "person"):
                    PERSON_Stat = PERSON_Stat+ 1
                elif (tag == "dog"):
                    DOG_Stat = DOG_Stat+ 1
                elif(tag == "cat"):
                    CAT_Stat = CAT_Stat+ 1
                    

                # calculate the y-coordinate used to write the label on the
                # frame depending on the bounding box coordinate
                y = obj["ymin"] - 15 if obj["ymin"] - 15 > 15 else \
                    obj["ymin"] + 15

                # draw a bounding box rectangle and label on the frame
                cv2.rectangle(orig, (obj["xmin"], obj["ymin"]), (obj["xmax"],
                    obj["ymax"]), COLORS[obj["class_id"]], 2)
                cv2.putText(orig, label, (obj["xmin"], y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, COLORS[obj["class_id"]], 3)

            # display the current frame to the screen
            cv2.imshow("TinyYOLOv3", orig)

            # update the FPS counter
            fps.update()
            
            detectIterations = detectIterations + 1
            endTime = time.perf_counter()
            elapseTime = endTime - startTime #seconds
            print(elapseTime)

        # stop the timer and display FPS information
        fps.stop()
        print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        print("[INFO] Time Frame Calculation for Person: ", PERSON_Stat)
        print("[INFO] Time Frame Calculation for Dog: ", DOG_Stat)
        print("[INFO] Time Frame Calculation for Cat: ", CAT_Stat)

        #calculate confidence level
        print("Calculating OD Stats")
        IterationPercentage = elapseTimerTime / detectIterations
        print(IterationPercentage)

        DOG_Final= DOG_Stat * IterationPercentage
        print(DOG_Final)

        CAT_Final= CAT_Stat * IterationPercentage
        print(CAT_Final)

        PERSON_Final= PERSON_Stat * IterationPercentage
        print(PERSON_Final)

        if(((DOG_Final or CAT_Final) > confidenceTimeThreshold) and (PERSON_Final < confidenceTimeThreshold )):
            #pet is detected
            detectResult = True
            print("[INFO] Detection...")
            #print("detectResult = True")
        else :
            detectResult = False
            print("[INFO] No Detection...")
            resetVars()
            
    if (detectResult == True):
        #Close resources
        print("Reading TEMP")
        Current_Temp = readTemp()
        print(Current_Temp)
        #Publish to AWS
        publish_topic(outgoing_topic, Current_Temp)

        # stop the video stream and close any open windows1
        vs.stop() #if args["input"] is None else vs.release()
        cv2.destroyAllWindows()


###################################END OF FILE######################################

