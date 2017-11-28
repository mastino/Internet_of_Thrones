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
    def __init__(self, number, path, currPos):
        self.hiList = []
        self.lowList = False
        self.id = number
        self.name = "car" + str(number)
        self.goal = path
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
                    #send permission
                    pass
                else:
                    #appending car id to lowlist to send it permission afer we go
                    self.lowList.append(message[1])
            else: 
                #send permission
                pass
        elif message[0] == 'permission':
            # check if it is the car being given permission
            # remove from hilist
            # if hilist is empty then move into critical zone
            pass
        elif message[0] == 'moved':
            #maybe call like a goal(?) state 
            # if it is goal 
            pass
        else:
            print("not a valid message")
    # give permission to other cars
    def send_permission(carFrom, carTo):
        pass
    
    #have it send messages saying it needs to move?
    # possibly receive message saying to continue
    # maybe this should be a bool and this should be movenextspot
    # maybe this should queue the car
    # call exit_critical when done
    def enter_critical(carId, currentPos, goalPos):
        pass
    #sends permission to all cars in the low list
    def exit_critical(carId,lowlist):
        for car in lowlist:
            send_permission(carId, car)
    
    

#car platform and bcast 

def createCars(num):
    cars = []

    for i in range(num):
        cars.append(Car(i))
    return cars

while True:
    pass 


