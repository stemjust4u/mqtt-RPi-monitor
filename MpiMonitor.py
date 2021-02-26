from vcgencmd import Vcgencmd
from time import sleep, strftime, time
from os import path
from pathlib import Path
import paho.mqtt.client as mqtt
import sys, re, json

class PiMonitor():                                       # Pi T
    def __init__(self, logFile):
        # Initialize
        self.logDir = path.dirname(__file__)
        self.logFile = logFile
        Path(path.join(self.logDir, self.logFile)).touch(exist_ok = True)
        self.vcgm = Vcgencmd()

    # Update log
    def update_log(self, temp):
        with open(path.join(self.logDir, self.logFile), "a") as log:
            log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp)))

    # Get temperature
    def get_temp(self):
        temp = self.vcgm.measure_temp()
        return temp

# Main Loop
if __name__ == "__main__":
    # Import mqtt and wifi info. Remove if hard coding in python file
    home = str(Path.home())
    with open(path.join(home, "stem"),"r") as f:
        stem = f.read().splitlines()

    #=======   SETUP MQTT =================#
    MQTT_SERVER = '10.0.0.115'                    # Replace with IP address of device running mqtt server/broker
    MQTT_USER = stem[0]                           # Replace with your mqtt user ID
    MQTT_PASSWORD = stem[1]                       # Replace with your mqtt password
    MQTT_SUB_TOPIC1 = 'monitor/pi/instructions'   # Subscribe topic (incoming messages, instructions)
    MQTT_PUB_TOPIC1 = 'monitor/pi/temp'           # Publish topic (outgoing messages, data, instructions)
    MQTT_CLIENT_ID = 'argon1'                     # Give your device a name
    WIFI_SSID = stem[2]                           # Replace with your wifi SSID
    WIFI_PASSWORD = stem[3]                       # Replace with your wifi password

    # Define mqtt callback functions then link them to the mqtt callback below in main program
    # on connect callback verify a connection established and subscribe to TOPICs
    def on_connect(client, userdata, flags, rc):
        print("attempting on_connect")
        if rc==0:
            mqtt_client.connected = True          # If rc = 0 then successful connection
            client.subscribe(MQTT_SUB_TOPIC1)     # Subscribe to topic
            print("Successful Connection: {0}".format(str(rc)))
            print("Subscribed to: {0}".format(MQTT_SUB_TOPIC1))
        else:
            mqtt_client.failed_connection = True  # If rc != 0 then failed to connect. Set flag to stop mqtt loop
            print("Unsuccessful Connection - Code {0}".format(str(rc)))

        ''' Code descriptions
            0: Successful Connection
            1: Connection refused: Unacceptable protocol version
            2: Connection refused: Identifier rejected
            3: Connection refused: Server unavailable
            4: Connection refused: Bad user name or password
            5: Connection refused: Not authorized '''
            
    # on message callback will receive messages from the server/broker. Must be subscribed to the topic in "on_connect" 
    def on_message(client, userdata, msg):
        global dummy1, dummy2 # can define global variables
        #print(msg.topic + ": " + str(msg.payload)) # Uncomment for debugging
        dummyD = json.loads(str(msg.payload.decode("utf-8", "ignore")))  # decode the msg to json and convert to python dictionary
        dummy1 = dummyD['aaa']
        dummy2 = dummyD['bbb']

    # on publish will send data to client
    def on_publish(client, userdata, mid):
        #print("mid: " + str(mid)) # Uncomment for debugging
        pass

    #==== start/bind mqtt functions ===========#
    mqtt.Client.connected = False         # Flag for initial connection (different than mqtt.Client.is_connected)
    mqtt.Client.failed_connection = False # Flag for failed initial connection
    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect  #bind call back function
    mqtt_client.on_message = on_message  #bind function to be used when PUBLISH messages are found
    mqtt_client.on_publish = on_publish  #bind function for publishing
    mqtt_client.loop_start()   # other option is client.loop_forever() but it is blocking
    print("Connecting to: {0}".format(MQTT_SERVER))
    mqtt_client.connect(MQTT_SERVER, 1883)  # connect to the mqtt. this is a blocking function. script will stop while connecting.
    while not mqtt_client.connected and not mqtt_client.failed_connection:
        print("Waiting")
        sleep(1)
    if mqtt_client.failed_connection:
        mqtt_client.loop_stop()
        sys.exit()

    pi1 = PiMonitor("temp-log.txt")
    while True:
        cpuTemp = pi1.get_temp()
        mqtt_client.publish(MQTT_PUB_TOPIC1, str(cpuTemp)) 
        pi1.update_log(cpuTemp)
        sleep(1)