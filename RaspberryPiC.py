# for handling CTRL+C
import signal

# for getting command line arguments
import sys, getopt

# for MQTT
import paho.mqtt.client as mqtt

import time

TOPICS = [("lightSensor", 2), ("threshold", 2), ("LightStatus", 2)]

lastSensor = float(-1)
lastThreshold = float(-1)
lastStatus = None

# the IP address of the broker
broker_ip = '127.0.0.1' # default to localhost

# the MQTT client object
client = None

def main():
    global broker_ip, client
    # register the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # parse the command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:")
    except getopt.GetoptError:
        print('GET OPT ERROR')
    for opt, arg in opts:
        if opt == '-i':
            broker_ip = arg

    print('Connecting to broker at: ' + broker_ip)
    client = mqtt.Client("RaspberryPiC")
    client.on_connect = on_connect
    client.on_message = on_message
    client.will_set("Status/RaspberryPiC", "offline", qos=2, retain=True )
    client.connect(broker_ip, keepalive = 10)
    client.loop_start()
    while True:
        pass

def on_connect(client,userdata,flags,rc):
    print("Connected to broker at: " + broker_ip)
    client.subscribe(TOPICS) # subscribe to our topics
    client.publish("Status/RaspberryPiC", 'online', qos=2, retain=True)

# Every time a message is recieved, it is checked if the value of the message for topic has changed since the last message. If it has, then it is changed
# The values from both topics are compared, and if the lgithSensor is less than the threshold, then the LED is turned on, otherwise, it is turned off
# Note: If this client hasn't recieved a message from both topics, the output will continue to be TurnOff
def on_message(client,userdata,msg):
    global lastSensor, lastThreshold, lastStatus
    
    if msg.topic == "LightStatus":
        print("Received from topic LightStatus")
        lastStatus = msg.payload.decode()
        return

    # If it recieves a input from the lightSensor topic, then it needs to check to see if the value has changed
    if msg.topic == "lightSensor":
        print("Recieved from topic lightSensor")
        lastSensor = float(msg.payload.decode())
        print(lastSensor)
    
    # If it recieves a input from the Threshold topic, then it needs to check to see if the value has changed
    if msg.topic == "threshold":
        print("Recieved from topic threshold")
        lastThreshold = float(msg.payload.decode())
        print(lastThreshold)

    # if the sensor is greater than the threshold
    if lastSensor >= lastThreshold:
        print("lastSensor >= lastThreshold")
        # TurnOn, but only if the the lastStatus is TurnOff
        if lastStatus == None or str(lastStatus) != "TurnOn":
            # then publish
            print("Turning the light on 1")
            client.publish("LightStatus", payload="TurnOn", qos=2, retain=True)
            lastStatus = "TurnOn"
            print("Turning the light on 2")
    else:
        print("lastSensor < lastThreshold")
        # TurnOff, but only if the lastStatus is TurnOn
        if lastStatus == None or str(lastStatus) != "TurnOff":
            print("Turning the light off 1")
            client.publish("LightStatus", payload="TurnOff", qos=2, retain=True)
            lastStatus = "TurnOff"
            print("Turning the light off 2")

# handle CTRL+C
def signal_handler(sig, frame):
    global client
    print('\nDisconnecting gracefully')
    if (client != None):
        client.publish("Status/RaspberryPiC", payload="offline", qos=2, retain=True) # publish that that RPI A is offline
        time.sleep(0.5)
        client.disconnect()
    # wait before ending the program
    time.sleep(0.5)
    sys.exit(0)


if __name__ == "__main__":
    main()

