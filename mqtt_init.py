import time, socket, sys
from datetime import datetime as dt
import paho.mqtt.client as paho
import signal

def on_connect(client, userdata, flags, rc):
    print('connected')

def on_disconnect(client, userdata, rc):
    print("Disconnected in a normal way")
    #graceful so won't send will

def on_log(client, userdata, level, buf):
    print("log: {}".format(buf)) # only semi-useful IMHO


def setup_mqtt(will_topic, will, on_message):
    # Instantiate the MQTT client
    mqtt_client = paho.Client()

    # set up handlers
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_log = on_log

    mqtt_client.will_set(will_topic, will, 0, False)
 
    broker = 'sansa.cs.uoregon.edu'  # Boyana's server
    mqtt_client.connect(broker, '1883')

    return mqtt_client
