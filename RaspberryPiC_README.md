# Raspberry Pi C README

*All of the code was written using Python 3.  If the code is not running correctly, then make sure that you are using Python 3.  If Python 3 is not your default Python installation, then you will need to use the `pip3` command instead of `pip` and the `python3` command instead of `python`.*

RaspberryPiC.py requires the Python Paho MQTT client library.  Make sure that it is installed by following the steps below:
1. Run `pip install paho-mqtt`.

The RaspberryPiC.py program accepts a command line argument for the broker's IP address.  It is specified by using the `-i` argument.  You can run the program by running the following command:
`python RaspberryPiC.py -i <IP_ADDRESS_HERE>`

You can end the program gracefully by pressing CTRL + C.
