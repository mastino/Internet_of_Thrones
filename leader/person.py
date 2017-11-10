import atexit, sys
from mqtt_client import MQTTClient

class Person(MQTTClient):

    def __init__(self, max_sitting):
        super(Person, self).__init__()
        self.id = int(max_sitting)
        self.currently_sitting = set([])
        self.subscribe('butler')

    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        topic = msg.topic.split('/')[-1]
        msg_parts = msg.payload.split(':')
        
        if topic == 'cmd':
            msg_parts = msg.payload.split(':')
            action, nid, lid = msg_parts[0], msg_parts[1], msg_parts[1]
            if mqtt_client.id == nid:
                mqtt_client.process_cmd(action, lid)

        else: ## topic == log
            msg = msg.payload

        return

    def process_cmd(self, action, lid):
        if action == 'election':
            pass
        elif action == 'announce':
            pass
        return

    def send_arise(self, phil_id):
        if phil_id in self.currently_sitting:
            self.currently_sitting.remove(phil_id)
            self.publish('phil_' + phil_id, 'arise')
        return

# at exit function
def cleanup(client):
    client.disconnect()
    client.loop_stop()

# do butler stuff
person = Person(sys.argv[1])
atexit.register(cleanup, person)
while True:  # block
    pass
