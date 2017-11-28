import atexit
from mqtt_client import MQTTClient
class Instruction(MQTTClient):
    def __init__(self):
        super(Instruction,self).__init__()
        self.subscribe("car")
    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        msg_parts = msg.payload.split(':')
        if msg_parts[0] == 'move':
            car, direction, spot = msg_parts[1], msg_parts[2], msg_parts[3]
            print("move car" + car  + " " + direction + " to spot " + spot)
            raw_input("Press enter to continue")
            self.publish("car", "moved:" + car + ":" + spot)
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
