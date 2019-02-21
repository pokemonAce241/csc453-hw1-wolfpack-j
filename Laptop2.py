# for MQTT
import paho.mqtt.client as mqtt

# for time stamps
import datetime

# for handling CTRL+C
import signal, time

# for getting command line arguments
import sys, getopt

# the topics to subscribe to
TOPICS = [("LightStatus", 2), ("Status/RaspberryPiA", 2), ("Status/RaspberryPiC", 2), ("threshold", 2), ("lightSensor", 2)]

# the name of the file where the logs will be written
OUTPUT_FILE_NAME = "message_log.txt"

# the file object used to write data
file = None

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

    client = mqtt.Client("Laptop2")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_ip)
    client.loop_start()
    while True:
        pass

def on_connect(client, userdata, flags, rc):
        global file
        print("Connected to broker at: " + broker_ip)
        file = open(OUTPUT_FILE_NAME, "w")
        client.subscribe(TOPICS)

def on_message(client, userdata, msg):
    global file
    log = str(datetime.datetime.now())
    if msg.topic == "LightStatus":
        log = log + " LightStatus: " + str(msg.payload.decode())
    if msg.topic == "Status/RaspberryPiA":
        log = log + " Status/RaspberryPiA: " + str(msg.payload.decode())
    if msg.topic == "Status/RaspberryPiC":
        log = log + " Status/RaspberryPiC: " + str(msg.payload.decode())
    if msg.topic == "threshold":
        log = log + " threshold: " + str(msg.payload.decode())
    if msg.topic == "lightSensor":
        log = log + " lightSensor: " + str(msg.payload.decode())

    # print out the log and write it to the file
    print(log)
    file.write(log + "\n")

# handle CTRL+C
def signal_handler(sig, frame):
    global client
    print('\nDisconnecting gracefully')
    if (client != None):
        client.disconnect()
    if (file != None):
        file.close()
    # wait before ending the program
    time.sleep(0.5)
    sys.exit(0)

if __name__ == "__main__":
    main()
