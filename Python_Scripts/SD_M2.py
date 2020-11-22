##Main control program for microncontroller M2 
##for California State Univ Fresno Senior Design 186B 2020
##by James Dols and Daniel Jacuinde


#python-can libarary
import can
#Text and SMS messages
import NotificationFeature
##necessary dependicies for interaction with AWS IoT Core
import argparse
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time
from uuid import uuid4

#intilize variables
received_count = 0 
publish_count = 0
received_all_event = threading.Event()
lastsendtime = 0.0
global finish
finish = False

incoming_topic = 'SD_M1/temp/details'
outgoing_topic = 'SD_M2/recheck/details'
outgoing_message = 'Check again'

##Function definitions.
# Callback when connection is accidentally lost.
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
    global current_temp
    global finish
    print("Received message from topic '{}': {}".format(topic, payload))
    topic_parsed = False
    if "/" in topic:
        parsed_topic = topic.split("/")
        if len(parsed_topic) == 3:
            # this topic has the correct format
            if (parsed_topic[0] == 'SD_M1') and (parsed_topic[2] == 'details'):
                # this is a topic we care about, so check the 2nd element
                if (parsed_topic[1] == 'temp'):
                    print("Received temperature reading: {}".format(payload))
                    current_temp = float(payload)  ##Convert the received string into a float. 
                    if current_temp == -999.0:##recieving a payload value of -999.0 will cause the session to disconnect.
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
     
##END Function definitions.#######################333

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
    client_id="SD_M2-" + str(uuid4()),
    clean_session=False,
    keep_alive_secs=6)
##Redefined endpoint and client as local variables##This is not strictly needed except for print statement.    
endpoint='a3f97mcy639kgs-ats.iot.us-east-2.amazonaws.com'
client_id="SD_M2-" + str(uuid4())

print("Connecting to {} with client ID '{}'...".format(endpoint, client_id))

connect_future = mqtt_connection.connect()

# Future.result() waits until a result is available
connect_future.result()
print("Connected!")
#########Main code goes below #####################################

##Subscribes to the topic
subscribe(incoming_topic)

###bring up the virtual can bus
bus = can.Bus(interface = 'socketcan',channel ='vcan0',receive_own_messages=True)


### start main loop
while not finish:
    incount = 1
    # Wait for all messages to be received.
    #This waits forever if incount was set to 0.
    if incount != 0 and not received_all_event.is_set():
        print("Waiting for all messages to be received...")

    received_all_event.wait()
    print("{} message(s) received.".format(received_count))


    if time.time()-lastsendtime > 120: #prevents spamming notifications
        print('At least two minutes have past')
        print('Sending a notification to the registered owner')
        ##N = Notification
        ##N.sendNotification('djacuinde96@gmail.com', '5597045940', 'att')
        lastsendtime =time.time()
    else:
        print('Too soon to send another notification')

    if current_temp > 80.5:
        print('Turning on the AC')
        message = can.Message(arbitration_id=392, is_extended_id=False,data =[0x03])## set this to desired message to turn on AC
        bus.send(message, timeout=0.2) ##transmits the message.
    else:
        message = can.Message(arbitration_id=392, is_extended_id=False,data =[0x00])## set this to desired message to turn off AC
        bus.send(message, timeout=0.2) ##transmits the message.
        print('Temp is ok, no action needed')

    time.sleep(1)  #sleep then send a message back to M1

    publish_topic(outgoing_topic,outgoing_message)
    received_all_event.clear()##reset wait for received.
    received_count = 0 ##reset received_count
##End main loop

# Disconnect
print("Disconnecting...")
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
print("Disconnected!")
