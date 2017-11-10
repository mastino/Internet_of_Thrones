import atexit, sys
from mqtt_client import MQTTClient

class Person(MQTTClient):

    def __init__(self, own_id, next_id):
        super(Person, self).__init__()
        self.own_id = int(own_id)
        self.next_id = int(next_id)
        self.subscribe('cmd')

    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        topic = msg.topic.split('/')[-1]
        msg_parts = msg.payload.split(':')

        if topic == 'cmd':
            msg_parts = msg.payload.split(':')
            action, nid, lid = msg_parts[0], msg_parts[1], msg_parts[1]
            if mqtt_client.own_id == nid:
                mqtt_client.process_cmd(action, lid)

        else: ## topic == log
            msg = msg.payload

        return

    def process_cmd(self, action, lid):
        if action == 'election':
            if   self.own_id >  lid:
                self.publish("cmd", "election:" + str(nid) + ":" + str(self.own_id))
            elif self.own_id <  lid:
                self.publish("cmd", "election:" + str(nid) + ":" + str(lid))
            elif self.own_id == lid:
                self.publish("cmd", "announce:" + str(nid) + ":" + str(self.own_id))

        elif action == 'announce':
            if self.own_id == lid:
                self.publish("log", "all informed")
            else:
                self.publish("cmd", "announce:" + str(nid) + ":" + str(lid))

            self.publish("log", str(self.own_id) + " doing real work")

        return


# at exit function
def cleanup(client):
    client.disconnect()
    client.loop_stop()

# do butler stuff
person = Person(sys.argv[1], sys.argv[2])
atexit.register(cleanup, person)
while True:  # block
    pass
