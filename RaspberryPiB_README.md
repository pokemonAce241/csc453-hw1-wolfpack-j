# Raspberry Pi B README

*All of the code was written using Python 3.  If the code is not running correctly, then make sure that you are using Python 3.  If Python 3 is not your default Python installation, then you will need to use the `pip3` command instead of `pip` and the `python3` command instead of `python`.*

RaspberryPiB.py requires the Python Paho MQTT client library.  Make sure that it is installed by following the steps below:
1. Run `pip install paho-mqtt` in the terminal

RaspberryPiB.py requires the RPi.GPIO library.  Make sure that it is installed by following the steps below:
1. Run `sudo apt-get update` in the terminal
2. Run `sudo apt-get install rpi.gpio` in the terminal
Or you can do the following:
1. Run `pip install RPI.GPIO`

The RaspberryPiB.py program contains a constant called MQTT_BROKER which holds the IP address of the MQTT broker.  If the broker that you're connecting to has changed its IP address, then you must edit this constant to reflect the correct IP address.

You can run the program by running the following command:
`python RaspberryPiB.py`
