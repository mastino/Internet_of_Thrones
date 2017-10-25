'''
fluent.py

test thingys for th butler project
input id when you start
python fluent.py [id]

'''

import atexit, time, sys
# import mraa
from mqtt_client import MQTTClient
from time import sleep

class Fluent(MQTTClient):

    def __init__(self, id_in, led_enable):
        super(Fluent, self).__init__()
        self.id     = id_in
        self.led    = int(id_in) + 2
        self.led_en = led_enable
        self.fluent = False
        self.subscribe('#')

    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        # print msg.topic, msg.payload
        topic = msg.topic.split('/')[-1]

        topic_l = topic.split('_')
        topic = topic_l[0]
        topic_id = "-1"
        if len(topic_l) > 1:
            topic_id = topic_l[1]

        # print "tpic id", type(topic_id), topic_id
        # print "tpic id", type(mqtt_client.id), mqtt_client.id

        if topic == "butler":
            msg_parts = msg.payload.split(':')
            action, id_option = msg_parts[0], msg_parts[1]
            if id_option == mqtt_client.id:
                if action == 'arise':
                    mqtt_client.off()
        elif (topic == "phil") and (topic_id == mqtt_client.id):
            action = msg.payload
            if action == 'sit':
                mqtt_client.on()

        return

    def on(self):
        self.fluent = True
        if self.led_en:
            led = mraa.Gpio(car.ledNum)
            led.dir(mraa.DIR_OUT)
            led.write(0)
        else:
            print "Fluent ", self.id, " ON"

    def off(self):
        self.fluent = False
        if self.led_en:
            led = mraa.Gpio(car.ledNum)
            led.dir(mraa.DIR_OUT)
            led.write(1)
        else:
            print "Fluent ", self.id, " OFF"
        

argc = len(sys.argv)
# print "argc: ", argc

if argc >= 2:
    id=sys.argv[1]
else:
    print "\nERROR\n\n"

if argc >= 3:
    led_enable = sys.argv[2] == "True"
else:
    led_enable = True

print "led enabled: ", led_enable

f = Fluent(id, led_enable)

while True:  # block
    try:
        pass
    except KeyboardInterrupt:
        print "\nbye"
        break


