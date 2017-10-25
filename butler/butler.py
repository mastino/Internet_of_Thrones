import atexit, sys
from mqtt_client import MQTTClient

class Butler(MQTTClient):

    def __init__(self, max_sitting):
        super(Butler, self).__init__()
        self.max_sitting = int(max_sitting)
        self.currently_sitting = set([])
        self.subscribe('butler')

    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        topic = msg.topic.split('/')[-1]
        msg_parts = msg.payload.split(':')
        action, id_option = msg_parts[0], msg_parts[1:]
        if action == 'sit':
            mqtt_client.send_sit(id_option[0])
        elif action == 'arise':
            mqtt_client.send_arise(id_option[0])
        return

    def send_sit(self, phil_id):
        if len(self.currently_sitting) < self.max_sitting:
            self.currently_sitting.add(phil_id)
            self.publish('phil_' + phil_id, 'sit')
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
butler = Butler(sys.argv[1])
atexit.register(cleanup, butler)
while True:  # block
    pass
