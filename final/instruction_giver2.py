import atexit, time
from mqtt_client import MQTTClient
class Instruction(MQTTClient):
    def __init__(self):
        super(Instruction,self).__init__()
        self.subscribe("car")
        self.outlist = []
    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        msg_parts = msg.payload.split(':')
        if msg_parts[0] == 'move':
            car, direction, spot = msg_parts[1], msg_parts[2], msg_parts[3]
            mqtt_client.outlist.append((car, direction, spot))
        return

    def dump_outlist(self):
        if not self.outlist:
            return
        temp_outlist = self.outlist[:]
        self.outlist = []
        for car, direction, spot in temp_outlist:
            print("move car" + car  + " " + direction + " to spot " + spot)
            self.publish("car", "moved:" + car + ":" + spot)
        raw_input("Press enter to continue")

# at exit function
def cleanup(client):
    client.disconnect()
    client.loop_stop()

# do turnstile stuff
inst = Instruction()
atexit.register(cleanup, inst)


while True:  # block
    inst.dump_outlist()
    time.sleep(1)
