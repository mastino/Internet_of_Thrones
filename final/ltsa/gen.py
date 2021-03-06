'''
Code to generate LTSA for the car project
Brian Gravelle
'''

MAX_CARS = 4

file = open("testfile.txt","w")


file.write("wait response do not use!!")
file.write("\n")
file.write("\n")
file.write("\n")

lower_priority = \
"""{2}receive_request[{0}][ID][Lanes] -> send_permission[ID][{0}] -> WAIT_RESPONSE{1}[ll2][ll3][ll4][l] |
"""

lower_priority1 = \
"""{2}receive_permission[{0}][ID] -> WAIT_RESPONSE{1}[ll2][ll3][ll4][l] |
"""

low_list = ["", "[{}][hl3][hl4]","[hl2][{}][hl4]","[hl2][hl3][{}]"]

for i in range(1,MAX_CARS+1):
    file.write("\n")
    cnt = i
    cnt1 = 1
    when_str = "when (ID == {}) ".format(i)
    for j in range(1,MAX_CARS+1):
        if i < j:
            file.write(lower_priority.format(j, low_list[cnt].format("True"), when_str))
            cnt+=1
        if i != j:
            file.write(lower_priority1.format(j, low_list[cnt1].format("False"), when_str))
            cnt1+=1

file.write("\nwhen(!hl2 && !hl3 && !hl4) time_out[ID] -> WAIT_PERMISSION[hl2][hl3][hl4][ll2][ll3][ll4][l]")

file.write("\n")
file.write("\n")
file.write("\n")
file.write("wait permission")
file.write("\n")
file.write("\n")
file.write("\n")

file.write("when(!hl2 && !hl3 && !hl4) enter[ID] -> CRITICAL[ll2][ll3][ll4][l] |  // not waiting for anyone\n")

lower_priority = \
"""{2} receive_permission[{0}][ID] -> WAIT_PERMISSION{1}[ll2][ll3][ll4][l] |
"""

low_list  = ["", "[{}][hl3][hl4]","[hl2][{}][hl4]","[hl2][hl3][{}]"]
low_list2 = ["", "[{}][ll3][ll4]","[ll2][{}][ll4]","[ll2][ll3][{}]"] 
when_lst = ["", "hl2", "hl3", "hl4"]


for i in range(1,MAX_CARS):
    file.write("\n")
    cnt = i
    for j in range(1,MAX_CARS+1):
        when_str = "when (ID == {} && {}) ".format(i, when_lst[cnt])
        if i < j:
            file.write(lower_priority.format(j, low_list[cnt].format("False"),  when_str))
            cnt+=1

lower_priority = \
'''{2} receive_request[{0}][ID][Lanes] -> WAIT_PERMISSION[hl2][hl3][hl4]{1} |
'''
for i in range(1,MAX_CARS+1):
    file.write("\n")
    cnt = 1
    when_str = "when (ID == {}) ".format(i)
    for j in range(1,MAX_CARS+1):
        if i != j:
            file.write(lower_priority.format(j, low_list2[cnt].format("True"),  when_str))
            cnt+=1

file.write("\n")
file.write("\n")
file.write("\n")
file.write("critical")
file.write("\n")
file.write("\n")
file.write("\n")

lower_priority = \
"""{2} receive_request[{0}][ID][Lanes] -> CRITICAL{1}[l] |
"""

low_list2 = ["", "[{}][ll3][ll4]","[ll2][{}][ll4]","[ll2][ll3][{}]"]

for i in range(1,MAX_CARS+1):
    file.write("\n")
    cnt = 1
    when_str = "when (ID == {}) ".format(i)
    for j in range(1,MAX_CARS+1):
        if i != j:
            file.write(lower_priority.format(j, low_list2[cnt].format("True"),  when_str))
            cnt+=1

file.write("""\nexit[ID] -> CLEANUP[ll2][ll3][ll4][l] |
go_slow[ID] -> CRITICAL[ll2][ll3][ll4][l]""")


file.write("\n")
file.write("\n")
file.write("\n")
file.write("cleanup")
file.write("\n")
file.write("\n")
file.write("\n")



lower_priority = \
"""{2} send_permission[ID][{0}] -> CLEANUP{1}[l] |
"""

low_list2 = ["", "[{}][ll3][ll4]","[ll2][{}][ll4]","[ll2][ll3][{}]"]
when_lst = ["", "ll2", "ll3", "ll4",""]

for i in range(1,MAX_CARS+1):
    file.write("\n")
    cnt = 1
    for j in range(1,MAX_CARS+1):
        when_str = "when (ID == {} && {}) ".format(i, when_lst[cnt])
        if i != j:
            file.write(lower_priority.format(j, low_list2[cnt].format("False"),  when_str))
            cnt+=1


file.write("""\nwhen(!ll2 && !ll3 && !ll4) restarting[ID] -> STARTUP |""")



file.write("\n")
file.write("\n")
file.write("\n")
file.write("sendall")
file.write("\n")
file.write("\n")
file.write("\n")

lower_priority = \
"""{1} send_request[ID][{0}][l] -> SENDALL[a][b][c][cnt-1] |
"""

for i in range(1,MAX_CARS+1):
    file.write("\n")
    cnt = i
    for j in range(1,MAX_CARS+1):
        when_str = "when (ID == {} && cnt > 0) ".format(i)
        if i != j:
            file.write(lower_priority.format(j, when_str))
            cnt+=1


file.write("""\nwhen(cnt == 0) dummy[ID] -> BCAST""")

file.close()