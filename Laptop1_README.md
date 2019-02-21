# Laptop 1 README

We used the Mosquitto MQTT broker on Laptop 1 and it required no configuration or custom code to work.  Simply install and run the broker on a Linux machine by following the steps below.
1. While in a terminal run `sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa`
2. Next run `sudo apt-get update`
3. Next run `sudo apt-get install mosquitto`

This is all that is required to install the broker itself. If you’d also like to install the testing clients, then run `sudo apt-get install mosquitto-clients`.  If more details are needed, here is the link to the tutorial that I followed to install Mosquitto on Linux: http://www.steves-internet-guide.com/install-mosquitto-linux/.

The broker will more than likely already be started as a system service once installed.  You can check on the status of the broker by running `sudo service mosquitto status`.
You can stop it by running `sudo service mosquitto stop`.
And start it again by running `sudo service mosquitto start`.
For debugging purposes, it’s useful to run the broker manually.  Make sure that the system service is stopped and then run the following command in a terminal to see all of the messages that are received and sent by the broker.
`mosquitto -v`
