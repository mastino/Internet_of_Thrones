# use python person.py [ID] [NID] <Initiate> <LED>
# ex  python person.py 0 1 False
# to specify LED you must specify initiate
#    both default to false

import atexit, sys, time
#import mraa
from mqtt_client import MQTTClient

class Person(MQTTClient):

    def __init__(self, own_id, next_id, init, led_enable):
        super(Person, self).__init__()
        self.own_id = int(own_id)
        self.next_id = int(next_id)
        self.subscribe('cmd')
        self.led_en = led_enable
        if self.led_en:
            self.led1 = mraa.Gpio(6)
            self.led2 = mraa.Gpio(7)
            self.led3 = mraa.Gpio(8)
        self.in_contention()

        if init:
            print "bad node"
            self.publish("cmd", "election:" + str(self.next_id) + ":" + str(self.own_id))
            self.publish("log", "passing:" + str(self.next_id) + ":" + str(self.own_id))
            self.id_sent = True
            self.publish("cmd", "announce:" + str(self.next_id) + ":" + str(self.own_id))
            self.publish("log", str(self.own_id) + " doing real work")
        else:
            self.id_sent = False


    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        # topic = msg.topic.split('/')[-1]
        # msg_parts = msg.payload.split(':')
        # if topic == 'cmd':
        #     msg_parts = msg.payload.split(':')
        #     action, nid, lid = msg_parts[0], int(msg_parts[1]), int(msg_parts[2])
        #     if mqtt_client.own_id == nid:
        #         mqtt_client.process_cmd(action, lid)
        #
        # else: ## topic == log
        #     msg = msg.payload

        return

    def process_cmd(self, action, lid):
        if action == 'election':
            if   (self.own_id >  lid) and not self.id_sent:
                self.publish("cmd", "election:" + str(self.next_id) + ":" + str(self.own_id))
                self.publish("log", "passing:" + str(self.own_id) + ":" + str(self.own_id))
                self.id_sent = True
            elif self.own_id <  lid:
                self.out_of_contention()
                self.publish("cmd", "election:" + str(self.next_id) + ":" + str(lid))
                self.publish("log", "passing:" + str(self.own_id) + ":" + str(lid))
            elif self.own_id == lid:
                self.leader()
                self.publish("cmd", "announce:" + str(self.next_id) + ":" + str(self.own_id))

        elif action == 'announce':
            if self.own_id == lid:
                self.publish("log", "all informed")
            else:
                self.publish("cmd", "announce:" + str(self.next_id) + ":" + str(lid))

            self.publish("log", str(self.own_id) + " doing real work")

        return

    def in_contention(self):
        if self.led_en:
            self.led1.dir(mraa.DIR_OUT)
            self.led1.write(0)
            self.led2.dir(mraa.DIR_OUT)
            self.led2.write(0)
            self.led3.dir(mraa.DIR_OUT)
            self.led3.write(1)
        else:
            print "Person ", self.own_id, " in contention"

        return

    def out_of_contention(self):
        if self.led_en:
            self.led1.dir(mraa.DIR_OUT)
            self.led1.write(0)
            self.led2.dir(mraa.DIR_OUT)
            self.led2.write(1)
            self.led3.dir(mraa.DIR_OUT)
            self.led3.write(1)
        else:
            print "Person ", self.own_id, " out of contention"

        return

    def leader(self):
        if self.led_en:
            self.led1.dir(mraa.DIR_OUT)
            self.led1.write(0)
            self.led2.dir(mraa.DIR_OUT)
            self.led2.write(0)
            self.led3.dir(mraa.DIR_OUT)
            self.led3.write(0)
        else:
            print "Person ", self.own_id, " declared leader"

        return


# at exit function
def cleanup(client):
    client.disconnect()
    client.loop_stop()

# do butler stuff
init = False
if len(sys.argv) >= 4:
    init = sys.argv[3] == "True"

led_enable = False
if len(sys.argv) >= 5:
    led_enable = sys.argv[4] == "True"

person = Person(sys.argv[1], sys.argv[2], init, led_enable)
atexit.register(cleanup, person)
while True:  # block
    pass
