##AWS IoT Core
import argparse
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time
from uuid import uuid4

####################################Functions########################################
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
                    if (Status == 'Complete'):
                        finish = True
                topic_parsed = True            
    if not topic_parsed:
            print("Unrecognized message topic.")
    global received_count
    received_count += 1
    if received_count == incount:
        received_all_event.set()

    
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
