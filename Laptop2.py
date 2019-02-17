import paho.mqtt.client as mqtt

import datetime

broker = "broker.hivemq.com"
broker = "iot.eclipse.org"

MQTT_TOPIC = [("LightStatus",2),("Status/RaspberryPiA",2),("Status/RaspberryPiC",2),("threshold",2),("lightSensor",2)]
MQTT_BROKER = "10.153.33.130"


def on_connect(client, userdata, flags, rc):
        print("connected with broker"+str(rc))
        client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
	print(datetime.datetime.now(), end=' ', flush=True)
	if msg.topic == "LightStatus":
		print("LightStatus: ",str(msg.payload.decode()))
	if msg.topic == "Status/RaspberryPiA":
		print("Status/RaspberryPiA: ",str(msg.payload.decode()))
	if msg.topic == "Status/RaspberryPiC":
		print("Status/RaspberryPiC: ",str(msg.payload.decode()))
	if msg.topic == "threshold":
		print("threshold: ",str(msg.payload.decode()))
	if msg.topic == "lightSensor":
		print("lightSensor: ",str(msg.payload.decode()))

client = mqtt.Client("Laptop2")
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER)
client.loop_start()
while True:
        pass
