import atexit
from mqtt_client import MQTTClient

# create the custom monitor client
class Monitor(MQTTClient):

    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
    	print "[[%s]] %s" % (msg.topic, msg.payload)

# at exit function
def monitor_cleanup(client):
    client.disconnect()
    client.loop_stop()

# do monitor stuff
monitor = Monitor()
atexit.register(monitor_cleanup, monitor)
monitor.subscribe('#')
while True:  # block
    pass
