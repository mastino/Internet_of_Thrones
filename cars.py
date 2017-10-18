import mraa, time, sys
import paho.mqtt.client as paho
import mqtt_client

N=3

class Car:
    def __init__(self, number):
        self.isRiding = False
        self.hasPassengers = False
        self.ledNum = number+2
        self.name = "car" + str(number)
    def ride(self):
        mqtt_.publish(self.name + ' riding')
        self.isRiding = True
        turnOnLed(self)
    def request(self):
        mqtt_.publish(self.name + ' requesting')
    def pickUp(self):
        mqtt_.publish(self.name + ' pickup')
        self.hasPassengers = False
    def dropOff(self):
        turnOffLed(self)
        mqtt_.publish(self.name + ' dropoff')
        self.hasPassengers = False
        self.isRiding = False

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

mqtt_= mqtt_client.MQTTClient()
#mqtt_.subscribe('control')

def on_message(client, userdata, msg, mqtt_client):
    print("here")
#on message 'ready for pick up' send request if not full or riding
#if recieves a message allowed to pick up, pick up and begin riding
#after some time drop off passengers

cars = createCars(3)
for car in cars:
    turnOnLed(car)



