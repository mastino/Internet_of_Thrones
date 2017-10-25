import mraa, sys
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
        topic = msg.topic.split('/')[-1]
        command, label = msg.payload.split(':') 
        if topic.startswith('phil'):
            _id = topic.split('_')[1]
            if label == self.name and command == 'get':
                getFork(_id)
            if label == self.name and command == 'put':
                turnOffLed(self.led)
                self.inUse = False
                #turnOffled
    def getFork(_id):
        if not self.inUse:
            turnOnLed(self.led)
            self.inUse = True
            self.publish('phil_'+ _id, 'get' + self.name)

    def putFork(_id):
        if self.inUse:
            self.inUse = False
            self.publish('phil_'+ _id, 'put' +self.name)

def turnOnLed(num):
    led = mraa.Gpio(num)
    led.dir(mraa.DIR_OUT)
    led.write(0)

def tunrOffLed(num):
    led = mraa.Gpio(num)
    led.dir(mraa.DIR_OUT)
    led.write(1)
Fork(sys.argv[1], sys.argv[2])
while True:
    pass 
            

    
            
