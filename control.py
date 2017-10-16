import time, socket, sys
from datetime import datetime as dt
import paho.mqtt.client as paho
import signal
import mqtt_init

class Control(object):
    """docstring for Control"""
    def __init__(self):
        self.mqtt_topic = "650/Internet_of_Things/"
        

# Deal with control-c
def control_c_handler(signum, frame):
    print('saw control-c')
    mqtt_client.disconnect()
    mqtt_client.loop_stop()  # waits until DISCONNECT message is sent out
    fi.close()
    print "Now I am done."
    sys.exit(0)

signal.signal(signal.SIGINT, control_c_handler)

# Get your IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_addr = str(s.getsockname()[0])
print('IP address: {}'.format(ip_addr))
s.close()

# The callback for when a PUBLISH message is received from the server that matches any of your topics.
# However, see note below about message_callback_add.
def on_message(client, userdata, msg):
    print('on_message')
    #print(client)
    #print(userdata)
    print(msg.topic)
    print(msg.payload)
    name = msg.payload.split('=')[-1].strip()
    if not (name in names):
        fi.write(name)
        fi.write("\n")
        names.append(name)


# You can subscribe to more than one topic: https://pypi.python.org/pypi/paho-mqtt#subscribe-unsubscribe.
# If you do list more than one topic, consdier using message_callback_add for each topic as described above.
# For below, wild-card should do it.
# TODO
mqtt_client.subscribe('cis650/#') #subscribe to all students in class

mqtt_client.loop_start()  # just in case - starts a loop that listens for incoming data and keeps client alive

while True:
    timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '==== '+MY_NAME  # don't change this or you will screw it up for others
    mqtt_client.publish(mqtt_topic, mqtt_message)  # by doing this publish, we should keep client alive
    time.sleep(3)

# I have the loop_stop() in the control_c_handler above. A bit kludgey.