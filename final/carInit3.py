# create 8 cars
"""        L3   EX2
         __ __ __ __
     EX3|  C  |  B  | Line 2
        |_____|_____|
        |  D  |  A  |
     L4 |__ __|__ __|  Exit 1
          E4    Line 1
"""

from cars import Car
import time

car0 = Car(0, 'EX1', 'L1')
car1 = Car(1, 'EX3', 'L3')
car2 = Car(2, 'EX2', 'L2')
car3 = Car(3, 'EX4', 'L4')

time.sleep(2)  # wait for the cars to get initialized

car0.ask_permission()
car1.ask_permission()
car2.ask_permission()
car3.ask_permission()

while True:
    pass
