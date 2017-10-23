'''
fluent.py

test thingys for th butler project
input id when you start
python fluent.py [id]

'''

import atexit, sys
from mqtt_client import MQTTClient

class Fluent(MQTTClient):

    def __init__(self, name, f1, f2):
        super(Fluent, self).__init__()
        self.id

    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        topic = msg.topic.split('/')[-1]
        if topic != "butler":
            topic = topic.split('_')[0]
            id_   = topic.split('_')[-1]

            msg_parts = msg.payload.split(':')
            action, id_option = msg_parts[0], msg_parts[1:]
            if action == 'get':
                mqtt_client.pickup_fork(id_option[0])
            elif action == 'put':
                mqtt_client.putdown_fork(id_option[0])
            elif action == 'sit':
                mqtt_client.standing = False
            elif action == 'arise':
                mqtt_client.standing = True
            return


# at exit function
def cleanup(client):
    client.disconnect()
    client.loop_stop()


# do philosopher stuff
num_phil = (len(sys.argv) - 1) / 2
phil_list = []
for i in range(1, num_phil * 2, 2):
    new_phil = Philosopher(i/2, sys.argv[i], sys.argv[i+1])
    phil_list.append(new_phil)
    atexit.register(cleanup, new_phil)

while True:  # block
    print_menu(phil_list)
    try:
        phil, action = raw_input("enter command: ").strip().split()
        phil = int(phil)
        handle_action(phil_list[phil], action)
    except KeyboardInterrupt:
        print "\nbye"
        break
    except:
        print "INVALID COMMAND!!"



id=int(sys.argv[1])