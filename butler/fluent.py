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

    def __init__(self, id_in):
        super(Fluent, self).__init__()
        self.id     = id_in
        self.led    = id_in + 2
        self.fluent = False
        self.subscribe('#')

    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        topic = msg.topic.split('/')[-1]

        topic_l = topic.split('_')
        if len(topic_l) > 1:
            topic_id = topic_l[1]
        topic = topic_l[0]

        if topic == "butler":
            msg_parts = msg.payload.split(':')
            action, id_option = msg_parts[0], msg_parts[1:]
            if id_option == mqtt_client.id:
                if action == 'eating':
                    mqtt_client.on()
                elif action == 'arise':
                    mqtt_client.off()
            return

    def on():
        self.fluent = True
        led = mraa.Gpio(car.ledNum)
        led.dir(mraa.DIR_OUT)
        led.write(0)

    def off():
        self.fluent = False
        led = mraa.Gpio(car.ledNum)
        led.dir(mraa.DIR_OUT)
        led.write(1)
        

argc = len(sys.argv)
print "argc: ", argc

if argc >= 2:
    id=int(sys.argv[1])
else:
    print "\nERROR\n\n"

if argc >= 3:
    led_enable = sys.argv[2] == "True"
else:
    led_enable = True

print "led enabled: ", led_enable

f = Fluent(id)

while True:  # block
    try:
        pass
    except KeyboardInterrupt:
        print "\nbye"
        break
    except:
        print "INVALID COMMAND!!"


