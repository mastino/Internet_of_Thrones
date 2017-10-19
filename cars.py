#import mraa, time, sys
import sys
import paho.mqtt.client as paho
from mqtt_client import MQTTClient
from threading import Thread
from time import sleep

N=int(sys.argv[1])
if N > 7:
    quit

class Car(MQTTClient):
    def __init__(self, number):
        self.isRiding = False
        self.hasPassengers = False
        self.ledNum = number+2
        self.name = "car" + str(number)
        super(Car,self).__init__()
        self.subscribe("car")
    def ride(self):
        self.publish('car',self.name + ' riding')
        self.isRiding = True
        turnOnLed(self)
    def request(self):
        self.publish('car', 'available:'+ self.name)
    def pickUp(self):
        self.publish('car',self.name + ' pickup')
        self.hasPassengers = False
    def dropOff(self):
        turnOffLed(self)
        self.publish('car', self.name + ' dropoff')
        self.hasPassengers = False
        self.isRiding = False
    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        message = msg.payload
        message = message.split(":")
        if message[0] == 'request':
            if mqtt_client.hasPassengers == False:
                mqtt_client.request()
        elif message[1] == mqtt_client.name:
            mqtt_client.pickUp()
            mqtt_client.ride()
            myThread = Thread(target=timeFunc, args=(mqtt_client,4))
            myThread.start()
        else:
            print("not message")

#car platform and bcast 
def timeFunc(car, num):
    sleep(num)
    car.dropOff()
def createCars(num):
    cars = []

    for i in range(num):
        cars.append(Car(i))
    return cars

def turnOnLed(car):
    led = mraa.Gpio(car.ledNum)
    led.dir(mraa.DIR_OUT)
    led.write(0)


def turnOffLed(car):
    led = mraa.Gpio(car.ledNum)
    led.dir(mraa.DIR_OUT)
    led.write(1)

#mqtt_.subscribe('control')
#on message 'ready for pick up' send request if not full or riding
#if recieves a message allowed to pick up, pick up and begin riding
#after some time drop off passengers

cars = createCars(N)
#for car in cars:
 #   turnOnLed(car)
while True:
    pass 


