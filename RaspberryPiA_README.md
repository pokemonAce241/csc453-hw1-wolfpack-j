# Raspberry Pi A README

*All of the code was written using Python 3.  If the code is not running correctly, then make sure that you are using Python 3.  If Python 3 is not your default Python installation, then you will need to use the `pip3` command instead of `pip` and the `python3` command instead of `python`.*

RaspberryPiA.py requires the Python Paho MQTT client library.  Make sure that it is installed by following the steps below:
1. Run `pip install paho-mqtt`.

RaspberryPiA.py requires the Adafruit_Blinka library which provides support for CircuitPython in Python 3.  You can install it by following the steps below:
1. Make sure that I2C and SPI are enabled on your Raspberry Pi.
2. Install the RPi.GPIO library by running `pip install RPI.GPIO`.
3. Install the Adafruit_Blinka library by running `pip install adafruit-blinka`.
For more detailed instructions see https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi.

RaspberryPiA.py requires the Adafruit MCP3xxx library.  You can install it by following the steps below:
1. Run `pip install adafruit-circuitpython-mcp3xxx`.
For more instructions see https://learn.adafruit.com/mcp3008-spi-adc/python-circuitpython.

The RaspberryPiA.py program accepts a command line argument for the broker's IP address.  It is specified by using the `-i` argument.  You can run the program by running the following command:
`python RaspberryPiA.py -i <IP_ADDRESS_HERE>`

The program will print any messages from the lightSensor and threshold topics (which it is also publishing).

You can end the program gracefully by pressing CTRL + C.
