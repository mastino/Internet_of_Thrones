import atexit, sys
from mqtt_client import MQTTClient

class Philosopher(MQTTClient):

    def __init__(self, name, f1, f2):
        super(Philosopher, self).__init__()
        self.name = str(name)
        self.standing = True
        self.left_fork = f1
        self.right_fork = f2
        self.has_left_fork = False
        self.has_right_fork = False
        self.subscribe('phil_' + self.name)

    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        topic = msg.topic.split('/')[-1]
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

    def get_left_fork(self):
        self.publish('fork_' + self.left_fork, 'get:' + self.name)

    def get_right_fork(self):
        self.publish('fork_' + self.right_fork, 'get:' + self.name)

    def put_left_fork(self):
        self.publish('fork_' + self.left_fork, 'put:' + self.name)

    def put_right_fork(self):
        self.publish('fork_' + self.right_fork, 'put:' + self.name)

    def eating(self):
        self.publish('butler', 'eating:' + self.name)

    def attempt_to_sit(self):
        self.publish('butler', 'sit:' + self.name)

    def attempt_to_arise(self):
        self.publish('butler', 'arise:' + self.name)

    def pickup_fork(self, fork_id):
        if fork_id == self.left_fork:
            self.has_left_fork = True
        elif fork_id == self.right_fork:
            self.has_right_fork = True

    def putdown_fork(self, fork_id):
        if fork_id == self.left_fork:
            self.has_left_fork = False
        elif fork_id == self.right_fork:
            self.has_right_fork = False

# at exit function
def cleanup(client):
    client.disconnect()
    client.loop_stop()

# print out the action menu
def print_menu():
    print "\nActions: sit, get_left, get_right, eat, put_left, put_right, arise"

# handle philosopher action
def handle_action(philosopher, action):
    if action == 'sit':
        if not philosopher.standing:
            print "Philosopher already sitting!"
            return
        philosopher.attempt_to_sit()
    elif action == 'get_left':
        if philosopher.standing:
            print "Philsopher isn't sitting!"
            return
        philosopher.get_left_fork()
    elif action == 'get_right':
        if philosopher.standing:
            print "Philsopher isn't sitting!"
            return
        philosopher.get_right_fork()
    elif action == 'eat':
        if not (philosopher.has_left_fork and philosopher.has_right_fork):
            print "Need forks to eat!"
            return
        philosopher.eating()
    elif action == 'put_left':
        if not philosopher.has_left_fork:
            print "Philsopher doesn't have left fork!"
            return
        philosopher.put_left_fork()
    elif action == 'put_right':
        if not philosopher.has_right_fork:
            print "Philsopher doesn't have right fork!"
            return
        philosopher.put_right_fork()
    elif action == 'arise':
        if philosopher.standing:
            print "Philosopher isn't sitting!"
            return
        elif philosopher.has_left_fork or philosopher.has_right_fork:
            print "Philosopher still has a fork!"
            return
        philosopher.attempt_to_arise()
    else:
        raise RuntimeError
    return


# do philosopher stuff
if len(sys.argv) != 4:
    print "Usage: python {} <{}> <{}> <{}>".format(sys.argv[0], "phil_id", "left_fork", "right_fork")
    sys.exit()
new_phil = Philosopher(sys.argv[1], sys.argv[2], sys.argv[3])
atexit.register(cleanup, new_phil)

while True:  # block
    print_menu()
    try:
        action = raw_input("Enter action: ").strip()
        handle_action(new_phil, action)
    except KeyboardInterrupt:
        print "\nbye"
        break
    except:
        print "INVALID COMMAND!!"
