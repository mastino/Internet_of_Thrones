import atexit, sys
from mqtt_client import MQTTClient

# create the custom turnstile client
class Turnstile(MQTTClient):

    counter = 0

    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        topic = msg.topic.split('/')[-1]
        payload = msg.payload

        if topic == 'turnstile' and payload == 'empty':
            print "0 passengers on the platform"
            mqtt_client.counter = 0

    def send_passenger(self):
        self.publish('turnstile', "incoming!")

# at exit function
def turnstile_cleanup(client):
    client.disconnect()
    client.loop_stop()

# do turnstile stuff
turnstile = Turnstile()
atexit.register(turnstile_cleanup, turnstile)
turnstile.subscribe('turnstile')
turnstile.subscribe('bcast')
while True:  # block
    raw_input("press enter for passenger arrival\n")
    if turnstile.counter < 3:
        turnstile.counter += 1
        turnstile.send_passenger()
    print turnstile.counter, "passengers on the platform"
