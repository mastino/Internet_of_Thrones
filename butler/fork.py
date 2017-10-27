import sys
import mraa
from mqtt_client import MQTTClient

class Fork(MQTTClient):

    def __init__(self, name, led):
        super(Fork, self).__init__()
        self.name = name
        self.inUse = False
        self.led = led
        self.subscribe('#')

    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        print "here"
        topic = msg.topic.split('/')[-1] 
        if topic.startswith('fork'):
            msg_parts = msg.payload.split(":")
            command, label = msg_parts[0], msg_parts[1:]
           
            if command == 'get':
                print "at get"
                _id = topic.split('_')[1]
                print "label 0", label[0]
                if _id == mqtt_client.name:
                    mqtt_client.getFork(label[0])
            if command == 'put':
                 _id = topic.split('_')[1]
                 if _id == mqtt_client.name :
#                     turnOffLed(mqtt_client.led)
                     mqtt_client.putFork(label[0])
                #turnOffled
    def getFork(self, _id):
        if not self.inUse:
            turnOnLed(self.led)
            self.inUse = True
            self.publish('phil_'+ _id, 'get:' + self.name)

    def putFork(self, _id):
        if self.inUse:
            turnOffLed(self.led)
	    self.inUse = False
            self.publish('phil_'+ _id, 'put:' +self.name)

def turnOnLed(num):
    led = mraa.Gpio(int(num))
    led.dir(mraa.DIR_OUT)
    led.write(0)

def turnOffLed(num):
    led = mraa.Gpio(int(num))
    led.dir(mraa.DIR_OUT)
    led.write(1)
for x in range(7):
    led = mraa.Gpio(x)
    led.dir(mraa.DIR_OUT)
    led.write(1)
Fork(sys.argv[1], sys.argv[2])
while True:
    pass 
            

    
            
