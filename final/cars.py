import sys
from mqtt_client import MQTTClient
from mapInit import carMap, colMap, pathCol

# initialize 
# each car takes in an ID PATH and STARTINGPOS
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
    allCars = []
    def __init__(self, number, goal, currPos):
        self.hiList = []
        self.lowList = []
        self.id = number
        self.goal = goal
        self.path = []
        self.currentPosition = currPos
        super(Car,self).__init__()
        self.subscribe("car")
        allCars.append((self.id, self.goal, self.currentPosition))
    
    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        message = msg.payload
        message = message.split(":")
        if message[0] == 'request':
            if pathCol((message[2],message[3]),(self.currentPosition, self.goal)):
                if int(message[1]) > int(self.id):
                    send_permission(message[1])
                else:
                    #appending car id to lowlist to send it permission afer we go
                    self.lowList.append(message[1])
            else: 
                send_permission(message[1])
                pass
        elif message[0] == 'permission' and message[2] == self.id:
            self.hiList.remove(message[1])
            if len(hiList) == 0:
                enter_critical()
        elif message[0] == 'moved' and message[1] == self.id:
            if self.goal == message[2]:
                exit_critical()
            else:
                next_move()
        else:
            print("not a valid message")
    # give permission to other cars
    def send_permission(carTo):
        self.publish("car", "permission:" + str(self.id) + ":" + str(carTo))
    
    def next_move():
        (direction, next) = self.path[0]
        self.path = self.path[1:]
        self.publish("car", "move:" + str(self.id) + ":" + str(direction) + ":" + str(next)) 
    
    def enter_critical():
        self.path = carMap[(self.currentPosition, self.goal)]
        next_move()
    #sends permission to all cars in the low list
    def exit_critical(carId,lowlist):
        for car in lowlist:
            send_permission(carId, car)
        #maybe have a messge that it has exited
    
    

#car platform and bcast 

def createCars(num):
    cars = []

    for i in range(num):
        cars.append(Car(i))
    return cars

while True:
    pass 


