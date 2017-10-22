import atexit
from mqtt_client import MQTTClient

# at exit function
def cleanup(client):
    client.disconnect()
    client.loop_stop()

# do turnstile stuff
tester = MQTTClient()
atexit.register(cleanup, tester)
while True:  # block
    topic = (raw_input("enter topic name:\n")).strip()
    msg = (raw_input("enter message:\n")).strip()
    tester.publish(topic, msg)
