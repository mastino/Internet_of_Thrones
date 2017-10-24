'''
fluent.py

test thingys for th butler project
input id when you start
python fluent.py [id]

'''

import atexit, mraa, time, sys
from mqtt_client import MQTTClient
from time import sleep

class Fluent(MQTTClient):

    def __init__(self, id_in):
        super(Fluent, self).__init__()
        self.id     = id_in
        self.led    = id_in + 2
        self.fluent = False

    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        topic = msg.topic.split('/')[-1]
        if topic == "butler":
            msg_parts = msg.payload.split(':')
            action, id_option = msg_parts[0], msg_parts[1:]
            if id_option == mqtt_client.id
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
        

id=int(sys.argv[1])
f = Fluent(id)

while True:  # block
    try:
        pass
    except KeyboardInterrupt:
        print "\nbye"
        break
    except:
        print "INVALID COMMAND!!"


