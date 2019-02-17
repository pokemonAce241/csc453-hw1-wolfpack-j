# for reading from MCP3008
import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# for handling CTRL+C
import signal

# for getting command line arguments
import sys, getopt

# for MQTT
import paho.mqtt.client as mqtt

# the minimum ADC value received from the LDR
MIN_LDR_VAL = 2400
# the maximum ADC value received from the LDR
MAX_LDR_VAL = 40128

# the minimum ADC value received from the potentiometer
MIN_POT_VAL = 0
# the maximum ADC value received from the potentiometer
MAX_POT_VAL = 65472

# the percent difference that the LDR should change in order to publish
LDR_THRESHOLD = 0.03
# the percent difference that the potentiometer should change in order to publish
POT_THRESHOLD = 0.01

# the topics that RaspberryPiA should subscribe to
TOPICS = [("lightSensor", 2), ("threshold", 2)]

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
    client = mqtt.Client(client_id="RaspberryPiA", clean_session=True)
    client.on_connect = on_connect
    client.on_message = on_message
    client.will_set("Status/RaspberryPiA", payload="offline", qos=2, retain=True) # lastwill message as a retained message with content "offline" to a topic "Status/RaspberryPiA".
    print(broker_ip)
    client.connect(host=broker_ip, keepalive=10) # tbcheck return then excute
    client.loop_start()
    
    query_hardware()


def query_hardware():
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # create analog channels for the LDR and potentiometer
    ldr = AnalogIn(mcp, MCP.P0)
    pot = AnalogIn(mcp, MCP.P1)

    last_ldr_val = 0.0
    last_pot_val = 0.0

    while True:
        # normalize
        cur_ldr_val = normalize_value(MIN_LDR_VAL, MAX_LDR_VAL, ldr.value)
        cur_pot_val = normalize_value(MIN_POT_VAL, MAX_POT_VAL, pot.value)
        # if either the LDR or potentiometer values are outside their thresholds
        if (beyond_threshold(last_ldr_val, cur_ldr_val, LDR_THRESHOLD) or beyond_threshold(last_pot_val, cur_pot_val, POT_THRESHOLD)):
            # publish current LDR and potentiometer values
            client.publish("lightSensor", payload=str(cur_ldr_val), qos=2, retain=True)
            client.publish("threshold", payload=str(cur_pot_val), qos=2, retain=True)
        # update values
        last_ldr_val = cur_ldr_val
        last_pot_val = cur_pot_val
        # wait 100 ms
        time.sleep(0.1)

# normalize a given value between the given min and max values
def normalize_value(min_val, max_val, val):
    return (val - min_val) / (max_val - min_val)

# return whether or not the given values are outside of the given threshold
def beyond_threshold(val1, val2, threshold):
    if (abs(val1 - val2) > threshold):
        return True
    return False

# handle MQTT messages
def on_message(param_client, userdata, message):
    if (message.topic == "lightSensor"):
        last_ldr_val = float(message.payload.decode("utf-8"))
        print("lightSensor topic: ", last_ldr_val)
    if (message.topic == "threshold"):
        last_pot_val = float(message.payload.decode("utf-8"))
        print("threshold topic: ", last_pot_val)

# handle MQTT connection confirmation
def on_connect(param_client, userdata, message, rc):
    print("Connected to broker at: " + broker_ip)
    client.subscribe(TOPICS) # subscribe to our topics
    client.publish("Status/RaspberryPiA", payload="online", qos=2, retain=True) # publish that RPI A is online

# handle CTRL+C
def signal_handler(sig, frame):
    global client
    print('\nDisconnecting gracefully')
    if (client != None):
        client.publish("Status/RaspberryPiA", payload="offline", qos=2, retain=True) # publish that that RPI A is offline
        time.sleep(0.5)
        client.disconnect()
    # wait before ending the program
    time.sleep(0.5)
    sys.exit(0)


if __name__ == "__main__":
    main()
