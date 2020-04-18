""" Case-study "Gas station modelling"
Contributors: Artyom Belov: 100%

"""
import random

gaspumps = []
gasprice = {"АИ-80": 40.0, "АИ-92": 41.20, "АИ-95": 44.45, "АИ-98": 45.85}
gasamount = {"АИ-80": 0, "АИ-92": 0, "АИ-95": 0, "АИ-98": 0}
clients = []

def gaspumpinfo():
    # printing info about gas pumps
    for y in range(0, len(gaspumps)):
        print("Автомат №", (gaspumps[y])["code"], "максимальная очередь:", (gaspumps[y])["maxline"], end="")
        print("Марки бензина:", end="")
        for b in range(0, len((gaspumps[y])["gastypes"])):
            print(((gaspumps[y])["gastypes"])[b], end="")
        print(" ->", "*" * int((gaspumps[y])["currentline"]), sep="")


# pulling pump info from azs.txt
with open("azs.txt", "r") as azs:
    lines = azs.readlines()
    for x in range(0, len(lines)):
        azsline = lines[x].split(" ")

        # checking for correct gas types
        for y in range(2, len(azsline)):
            if azsline[y] not in gasprice.keys():
                azsline.remove(azsline[y])

        # gaspump info format: code, max line, current line, gas types
        gaspumps.append = {"code": azsline[0], "maxline": azsline[1], "currentline": 0, "gastypes": azsline[2::]}


# getting client information
with open("input.txt") as file:
    inputlines = file.readlines()
    # file.close() to reduce memory usage in big projects?
    for x in range(0, len(inputlines)):
        inputline = inputlines[x].split(" ")
        # client info format: time of arrival, litres of gas, gas type
        clienttime = inputline[0].split(":")
        clienttime = clienttime[0] * 60 + clienttime[1]
        clients.append([clienttime, inputline[1], inputline[2]])

# arranging clients in timeline
clienttimes = []
sortedclients = []
for x in range(0, len(clients)):
    clienttimes.append((clients[x])[0])
for x in range(0, len(clients)):
    sortedclients.append(clients[min(clienttimes)])
    clienttimes.remove(min(clienttimes))
clients = sortedclients

# getting first current time
time = min(clienttimes)

# simulating
currentclients = []
dissatisfiedclients = 0
while time != max(clienttimes) + 1:

    # releasing clients which have filled up on gas
    while (currentclients[0])[0] == time:
        print("В",(int(currentclients[0])[0] / 60),":",(int(currentclient[0]))[0] - (int(currentclients[0])[0] / 60), "клиент", end='')
        currenttime = (currentclients[0])[0] - (currentclients[0])[3]
        print(int(currenttime/60),":",currenttime - int(currenttime/60),(currentclients[0])[2], end='')
        print((currentclients[0])[1], (currentclients[0])[3]," заправил свой автомобиль и покинул АЗС.")

        for y in range(0, len(gaspumps)):
            if (gaspumps[y])[0] == (currentclients[0])[4]:
                (gaspumps[y])['currentline'] -= 1
                break
        currentclients.remove(currentclients[0])
        gaspumpinfo()

    # determening whether a new client is serviceable
    while (clients[0])[0] == time:
        currentclient = clients.pop(clients[0])
        currentclient[1] = int(currentclient[1])

        if currentclient[2] in gasprice.keys():
            assignto = []
            for y in range(0, len(gaspumps)):
                if currentclient[2] in (gaspumps[y])['gastypes'] and (gaspumps[y])['currentline'] < (gaspumps[y])['maxline']:
                    assignto.append((gaspumps[y])['currentline'])
                else:
                    assignto.append(None)

            choice = None
            for y in range(0, len(assignto)):
                if assignto[y] is not None:
                    if choice < assignto[y]:
                        choice = assignto[y]
                    else: choice = assignto[y]

            print("В ", int(currentclient[0] / 60), ":", int(currentclient[0]) - int(currentclient[0] / 60), sep="",
                  end=" ")
            print(" новый клиент:", int(currentclient[0] / 60), ":", int(currentclient[0]) - currentclient * 60, sep="",
                  end="")
            print(currentclient[2], currentclient[1], addseconds, end="")

            # adding a client to dissatisfied clients if no gas pump assigned
            if choice is None:
                print(" не смог заправить автомобиль и покинул АЗС.")
                dissatisfiedclients += 1

            # adding a client to the list and the toll
            else:
                print(" встал в очередь к автомату", (gaspumps[(assignto[assignto.index(choice)])])["code"])
                addseconds = int(int(currentclient[1]) / 10)
                if float(currentclient[1]) % 10 > 0:
                    addseconds += 1

                randadd = random.random()
                if randadd < 0.33:
                    addseconds -= 1
                elif randadd > 0.66:
                    addseconds += 1
                if addseconds <= 0:
                    addseconds = 1

                # client info format: time of arrival, litres of gas, gas type, added seconds, gaspump code
                currentclient[0] = currentclient[0] + addseconds
                currentclient.append(addseconds)
                currentclient.append((gaspumps[(assignto[assignto.index(choice)])])["code"])
                currentclients.append(currentclient)

                (gaspumps[(assignto[assignto.index(choice)])])['currentline'] += 1
                gasamount[(currentclient[3])] += int(currentclient[2])
                gaspumpinfo()

        # if client's gas preference isn't in supplied gases - not our fault, not a dissatisfied client
        else:
            print("В ", int(currentclient[0] / 60), ":", int(currentclient[0]) - int(currentclient[0] / 60), sep="",
                  end=" ")
            print(" новый клиент:", int(currentclient[0] / 60), ":", int(currentclient[0]) - currentclient * 60, sep="",
                  end="")
            print(currentclient[2], currentclient[1], "не смог заправить автомобиль и покинул АЗС")
            gaspumpinfo()
    time += 1


# printing final results of the simulation
print("Итог:\nЛитров в сутки:")
for x in gasamount.keys():
    print(x, ":", gasamount[x], sep="")
sales = 0
for x in gasprice.keys():
    sales += float(gasprice[x]) * int(gasamount[x])
print("Общая сумма продаж за сутки:", sales, "рублей.")
print("Клиентов, покинувших АЗС, не заправив автомобиль из-за скопившейся очереди:", dissatisfiedclients)

