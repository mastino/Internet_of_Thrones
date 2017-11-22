import atexit
from mqtt_client import MQTTClient
class Instruction(MQTTClient):
    def __init__(self):
        super(Instruction,self).__init__()
        self.subscribe("move")
    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        topic = msg.topic.split('/')[-1]
        msg_parts = msg.payload.split(':')
        if topic == 'move':
            msg_parts = msg.payload.split(':')
            car, spot = msg_parts[0], msg_parts[1]
            print("move " + car +" to spot " + spot)
            raw_input("Press enter to continue")
        return

# at exit function
def cleanup(client):
    client.disconnect()
    client.loop_stop()

# do turnstile stuff
test = Instruction()
atexit.register(cleanup, test)


while True:  # block
    pass