import paho.mqtt.client as mqtt
import paho.mqtt.client as paho

import time

MQTT_TOPIC = [("lightSensor",2), ("threshold", 2), ("LightStatus", 2)]
MQTT_BROKER = "10.153.33.130"

lastSensor = float(-1)
lastThreshold = float(-1)
lastStatus = "TurnOff"

def on_connect(client,userdata,flags,rc):
    print("connected with broker")
    client.subscribe(MQTT_TOPIC)
    client.publish("Status/RaspberryPiC", 'online', qos=2, retain=True)

# Every time a message is recieved, it is checked if the value of the message for topic has changed since the last message. If it has, then it is changed
# The values from both topics are compared, and if the lgithSensor is less than the threshold, then the LED is turned on, otherwise, it is turned off
# Note: If this client hasn't recieved a message from both topics, the output will continue to be TurnOff
def on_message(client,userdata,msg):
    global lastSensor, lastThreshold, lastStatus

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
    
    if msg.topic == "LightStatus":
        print("Received from topic LightStatus")
        lastStatus = msg.payload.decode()


    # if the sensor is greater than the threshold
    if lastSensor >= lastThreshold:
        print("lastSensor >= lastThreshold")
        # TurnOn, but only if the the lastStatus is TurnOff
        if str(lastStatus) == "TurnOff":
            # then publish
            print("Turning the light on 1")
            client.publish("LightStatus", payload="TurnOn", qos=2, retain=True)
            print("Turning the light on 2")
    else:
        print("lastSensor < lastThreshold")
        # TurnOff, but only if the lastStatus is TurnOn
        if str(lastStatus) == "TurnOn":
            print("Turning the light off 1")
            client.publish("LightStatus", payload="TurnOff", qos=2, retain=True)
            print("Turning the light off 2")



if __name__ == "__main__":
    client = paho.Client("RaspberryPiC")
    client.on_connect = on_connect
    client.on_message = on_message
    client.will_set("Status/RaspberryPiC","offline",qos=2,retain=True )
    client.connect(MQTT_BROKER)
    client.loop_start()
    while True:
        pass

