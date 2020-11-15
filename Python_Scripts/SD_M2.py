##Main control program for microncontroller M1 
##for Cal State Univ Fresno Senior Design 186B 2020
##by James Dols and Daniel Jacuinde

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
    print("Received message from topic '{}': {}".format(topic, payload))
    topic_parsed = False
    if "/" in topic:
        parsed_topic = topic.split("/")
        if len(parsed_topic) == 3:
            # this topic has the correct format
            if (parsed_topic[0] == 'device') and (parsed_topic[2] == 'details'):
                # this is a topic we care about, so check the 2nd element
                if (parsed_topic[1] == 'temp'):
                    print("Received temperature request: {}".format(payload))
                    topic_parsed = True
                if (parsed_topic[1] == 'light'):
                    print("Received light request: {}".format(payload))
                    topic_parsed = True
    if not topic_parsed:
            print("Unrecognized message topic.")
    global received_count
    received_count += 1
    if received_count == args.count:
        received_all_event.set()
##END Function definitions.#######################333

##AWS IoT logging
#original line: io.init_logging(getattr(io.LogLevel, args.verbosity), 'stderr')
io.init_logging(getattr(io.LogLevel, io.LogLevel.NoLogs.name), 'stderr')

##connect to AWS

event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)


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
##Redefined endpoint and client as local variables##This is not strictly needed.    
endpoint='a3f97mcy639kgs-ats.iot.us-east-2.amazonaws.com'
client_id="SD_M2-" + str(uuid4())

print("Connecting to {} with client ID '{}'...".format(endpoint, client_id))

connect_future = mqtt_connection.connect()

# Future.result() waits until a result is available
connect_future.result()
print("Connected!")


"""
# Subscribe
print("Subscribing to topic '{}'...".format(args.topic))
subscribe_future, packet_id = mqtt_connection.subscribe(
    topic=args.topic,
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received)

subscribe_result = subscribe_future.result()
print("Subscribed with {}".format(str(subscribe_result['qos'])))
"""
# Publish message to server desired number of times.
# This step is skipped if message is blank.
# This step loops forever if count was set to 0.
"""
if args.message:
    if args.count == 0:
        print ("Sending messages until program killed")
    else:
        print ("Sending {} message(s)".format(args.count))

    publish_count = 1
    while (publish_count <= args.count) or (args.count == 0):
        message = "{} [{}]".format(args.message, publish_count)
"""
topic = 'TestTopic1'
message = 'Testing 1-2-3'
print("Publishing message to topic '{}': {}".format(topic, message))
mqtt_connection.publish(
    topic=topic,
    payload=message,
    qos=mqtt.QoS.AT_LEAST_ONCE)
time.sleep(1)
publish_count += 1
"""
# Wait for all messages to be received.
# This waits forever if count was set to 0.
if args.count != 0 and not received_all_event.is_set():
    print("Waiting for all messages to be received...")

received_all_event.wait()
print("{} message(s) received.".format(received_count))
"""
# Disconnect
print("Disconnecting...")
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
print("Disconnected!")
