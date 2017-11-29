import sys
from mqtt_client import MQTTClient
from mapInit import carMap, colMap, pathCol


# what about lines to enter the path (??)

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
    allCars = ["0","1","2","3"]
    def __init__(self, number, goal, currPos):
        self.hiList = allCars[:]
        self.lowList = []
        self.id = number
        self.hiList = self.hiList.remove(self.id)
        self.goal = goal
        self.path = []
        self.currentPosition = currPos
        super(Car,self).__init__()
        self.subscribe("car")
    
    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        message = msg.payload
        message = message.split(":")
        if message[0] == 'request':
            if message[1] == self.id:
                pass
            elif pathCol((message[2],message[3]),(mqtt_client.currentPosition, mqtt_client.goal)):
                if int(message[1]) > int(mqtt_client.id):
                    send_permission(message[1])
                else:
                    #appending car id to lowlist to send it permission afer we go
                    mqtt_client.lowList.append(message[1])
            else: 
                send_permission(message[1])
                pass
        elif message[0] == 'permission' and message[2] == mqtt_client.id:
            mqtt_client.hiList.remove(message[1])
            if len(hiList) == 0:
                enter_critical()
        elif message[0] == 'moved' and message[1] == mqtt_client.id:
            if mqtt_client.goal == message[2]:
                exit_critical()
            else:
                next_move()
        else:
            print("not a valid message")
    # give permission to other cars
    def send_permission(carTo):
        self.publish("car", "permission:" + str(self.id) + ":" + str(carTo))
    
    def next_move():
        (direction, nextPos) = self.path[0]
        self.path = self.path[1:]
        self.publish("car", "move:" + str(self.id) + ":" + str(direction) + ":" + str(nextPos)) 
    
    def enter_critical():
        self.path = carMap[(self.currentPosition, self.goal)]
        next_move()
    #sends permission to all cars in the low list
    def exit_critical():
        for car in self.lowList:
            send_permission(car)
        #maybe have a messge that it has exited

    def ask_permission():
        self.publish("car", "request:" + self.id + ":" + self.currentPosition + ":" + self.goal) 

while True:
    pass 


