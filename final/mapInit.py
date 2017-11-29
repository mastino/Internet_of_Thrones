"""        L3   EX2
         __ __ __ __
     EX3|  C  |  B  | Line 2
        |_____|_____|
        |  D  |  A  |
     L4 |__ __|__ __|  Exit 1
          EX4   Line 1
Two paths from each entrance depending on exit, either straight then right or
straight straight then straight

(L1, EX1)
(L1, EX2)
(L2, EX2)
(L2, EX3)
(L3, EX3)
(L3, EX4)
(L4, EX4)
(L4, EX1)

"""

L1= 'L1'
L2= 'L2'
L3= 'L3'
L4= 'L4'
EX1='EX1'
EX2='EX2'
EX3='EX3'
EX4='EX4'
carMap ={(L1, EX1):[('Straight', 'A'), ('Right', 'EX1')],
(L1, EX2):[('Straight', 'A'), ('Straight', 'B'), ('Straight', 'EX2')],
(L2, EX2):[('Straight', 'B'), ('Right', 'EX2')],
(L2, EX3):[('Straight', 'B'), ('Straight', 'C'), ('Straight', 'EX3')],
(L3, EX3):[('Straight', 'C'), ('Right', 'EX3')],
(L3, EX4):[('Straight', 'C'), ('Straight', 'D'), ('Straight', 'EX4')],
(L4, EX4):[('Straight', 'D'), ('Right', 'EX4')],
(L4, EX1):[('Straight', 'D'), ('Straight', 'A'), ('Straight', 'EX1')]}

colMap = {(L1, EX1):[(L1, EX2),(L4, EX1)],
(L1, EX2):[(L1, EX1),(L4, EX1),(L2,EX2),(L2,EX3)],
(L2, EX2):[(L1, EX2),(L2, EX3)],
(L2, EX3):[(L1, EX2),(L2,EX2),(L3,EX3),(L3,EX4)],
(L3, EX3):[(L2,EX3),(L3,EX4)],
(L3, EX4):[(L2,EX3), (L3,EX3), (L4,EX4),(L4,EX1)],
(L4, EX4):[(L4,EX1),(L3,EX4)],
(L4, EX1):[(L4,EX4),(L1,EX1),(L3,EX4),(L1,EX2)]}

#think about later
def pathCol(path1, path2):
    possibleCol = colMap.get(path1)
    return path2 in possibleCol
