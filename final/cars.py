import mraa, time, sys
import sys
import paho.mqtt.client as paho
from mqtt_client import MQTTClient
from threading import Thread
from time import sleep

# if you remove something from a hashtable in java it doesnt remove it from memory

# initialize 
# each car takes in an ID PATH
# hilist (start with everyone)
# hilist -> permission with priority before them (higher id) paths conflict (need to hear back from)
# if no conflict with path give permission
# lowlist -> once done driving send permissions
# hi list empty enter into conflict zone
# exit conflict zone send permissions to lowlist
# in conflict zone keep track of square and goal and then be able recieve messages
# that tell it when to move 
#car needs a next step method
class Car(MQTTClient):
    def __init__(self, number, path, currPos):
        self.hiList = []
        self.lowList = False
        self.id = number
        self.name = "car" + str(number)
        self.goal = path
        self.currentPosition = currPos
        super(Car,self).__init__()
        self.subscribe("car")
    
    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        message = msg.payload
        message = message.split(":")
        if message[0] == 'request':
            if mqtt_client.hasPassengers == False:
                mqtt_client.request()
        elif message[0]=='pickup' and message[1] == mqtt_client.name:
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

while True:
    pass 


