import atexit, sys
from mqtt_client import MQTTClient

class Philosopher(MQTTClient):

    def __init__(self, name, f1, f2):
        super(Philosopher, self).__init__()
        self.name = str(name)
        self.standing = True
        self.eating = False
        self.left_fork = f1
        self.right_fork = f2
        self.has_left_fork = False
        self.has_right_fork = False
        self.subscribe('butler')

    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        topic = msg.topic.split('/')[-1]
        payload = msg.payload

        print topic

    def get_left_fork(self):
        self.publish('fork_' + left_fork, 'get')

    def get_right_fork(self):
        self.publish('fork_' + right_fork, 'get')

    def put_left_fork(self):
        self.publish('fork_' + left_fork, 'put')
        self.has_left_fork = False

    def put_right_fork(self):
        self.publish('fork_' + right_fork, 'put')
        self.has_right_fork = False

    def eating(self):
        self.publish

# at exit function
def cleanup(client):
    client.disconnect()
    client.loop_stop()

# print out the action menu
def print_menu(phil_list):
    n = len(phil_list)
    print "\nThere are {} philosophers: {}".format(n, ', '.join(map(str, range(n))))
    print "Possible actions: sit, get_left, get_right, eat, put_left, put_right, arise"
    print "Command format: <philosopher number> <action>"

# handle philosopher action
def handle_action(philosopher, action):
    if action == 'sit':
        if not philosopher.standing:
            print "That philosopher can't sit!"
            return
        # ask butler if it's possible
        pass
    elif action == 'get_left':
        if philosopher.standing:
            print "Philsopher isn't sitting!"
            return
        philosopher.get_left_fork()  # needs to handle response from fork in on_message
    elif action == 'get_right':
        if philosopher.standing:
            print "Philsopher isn't sitting!"
            return
        philosopher.get_right_fork()  # needs to handle response from fork in on_message
    elif action == 'eat':
        if not (philosopher.has_left_fork and philosopher.has_right_fork):
            print "Need forks to eat!"
            return
        philosopher.publish('butler', "eating:" + self.name)
    elif action == 'put_left':
        if not philosopher.has_left_fork:
            print "Philsopher doesn't have left fork!"
            return
        philosopher.put_left_fork()
    elif action == 'get_right':
        if not philosopher.has_right_fork:
            print "Philsopher doesn't have right fork!"
            return
        philosopher.put_right_fork()


# do philosopher stuff
num_phil = (len(sys.argv) - 1) / 2
phil_list = []
for i in range(1, num_phil * 2, 2):
    new_phil = Philosopher(i/2, sys.argv[i], sys.argv[i+1])
    phil_list.append(new_phil)
    atexit.register(cleanup, new_phil)

while True:  # block
    print_menu(phil_list)
    phil, action = raw_input("enter command: ").strip().split()
    phil = int(phil)
    handle_action(phil_list[phil], action)
