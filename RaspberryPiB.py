import paho.mqtt.client as mqtt

import RPi.GPIO as GPIO
import time

broker = "broker.hivemq.com"
broker = "iot.eclipse.org"

# Declare what topics this client should be subscribed to
MQTT_TOPIC = [("LightStatus",2),("Status/RaspberryPiA",2),("Status/RaspberryPiC",2)]
# Declares the IP Address of the broker
MQTT_BROKER = "10.153.33.130"

# Sets up the various ports the Raspberry Pi will use to turn on and off the LED's
GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)

# Initializes each of the outputs to false to ensure the LED's start out as off
GPIO.output(5,False)
GPIO.output(13,False)
GPIO.output(26,False)

# Once the client connects, a debugging statement is printed and the client is subscibred
# to the topics declared in the MQTT_TOPIC array
def on_connect(client, userdata, flags, rc):
    print("connected with broker"+str(rc))
    client.subscribe(MQTT_TOPIC)

# This handles all the logic that controls whether the lights should be off or on
# The yellow light indicates whether it is dark enough in the room based on the comparision
#      between the threshold and the input from the LDR
# The other two lights indicate the online/offline status of Raspberry Pi A and Raspberry Pi C
def on_message(client, userdata, msg):
    # If a message has been published to the topic, LightStatus, check the message value
    if msg.topic == "LightStatus":
        # If the message value is TurnOn, then we know that it is dark enough in the room
        # and we should turn the light that indicates brightness (the yellow one) on
        if msg.payload.decode() == "TurnOn":
            GPIO.output(5,True)
            print("light on")
        # If the message value is TurnOff, then we know that is is too light in the room
        # and we should turn the light that indicates brightness (the yellow one) off
        if msg.payload.decode() == "TurnOff":
            GPIO.output(5,False)
            print("light off")
    # If a message has been published to the topic, RaspberryPiA, check the message value
    if msg.topic == "Status/RaspberryPiA":
        # If the message value is online, then Raspberry Pi A is online, and the second
        # LED should be turned on
        if msg.payload.decode() == "online":
            GPIO.output(13,True)
            print("RaspberryPiA online")
        # If the message value is offline, then Raspberry Pi A is offline, and the second
        # LED should be turned off
        if msg.payload.decode() == "offline":
            GPIO.output(13,False)
            print("RaspberryPiA offline")
    # If a message has been published to the topic, RaspberryPiC, check the message value
    if msg.topic == "Status/RaspberryPiC":
        # If the message value is online, then Raspberry Pi C is online, and the third
        # LED should be turned on
        if msg.payload.decode() == "online":
            GPIO.output(26,True)
            print("RaspberryPiC online")
        # If the message value is offline, the Raspberry Pi C is offline, and the third
        # LED should be turned off. Note that when Raspberry Pi C is offline, we are
        # unsure if the amount of light in the room is bright enough, and therefore also
        # turn the light indicating brightness off
        if msg.payload.decode() == "offline":
            GPIO.output(26,False)
            GPIO.output(5,False)
            print("RaspberryPiC offline")
    # Give the hardware time to react
    time.sleep(1)
    # Console output indicating what topic the message was recieved from, and what the
    # message was. Used mainly for dubugging
    print(msg.topic+" "+str(msg.payload.decode()))
    
# Initializes this as client, RaspberryPiB
client = mqtt.Client("RaspberryPiB")

# Tells this client what to do once connected to the broker
client.on_connect = on_connect
# Tells this client what to do once a message is recieved from the broker on any topic
client.on_message = on_message

# Connects this client with the appropriate broker. The two numbers are just two
# possible ports this client can connect to on the broker device
client.connect(MQTT_BROKER, 1883,60)


# Tells the program to continue to loop until a inturrupt is thrown from the command line
# Note: we could change this and include a switch on one of the Raspberry Pi's, which would
#       be pretty cool, but that's all extra stuff.
client.loop_forever()