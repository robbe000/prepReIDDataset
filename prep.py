import numpy as np
import cv2
import os

class VerwerkDataset:
    def __init__(self, name):
        self.name = name




def leesHoofdinput():
    #Hoofdinputfile inlezen en verwerken
    #Hierin zit info over de verschillende opnamens (state == 0)
    #en over welke koeien dezelfde zijn over de verschillende opnames heen (state == 1)
    hoofdInputFile = open("output/info.txt")

    opnames = []
    zelfde = []

    state=0
    for lijn in hoofdInputFile.readlines():
        if lijn.strip('\n') == "":
            state=1
        else:
            if state == 0:
                opnames.append(lijn.strip('\n'))
            else:
                zelfde.append((0, lijn.strip('\n').split()))

    return opnames, zelfde

def verwerkObject(opname, object, teller, objectTeller):
    infoFile = open("output/"+opname+"/"+object+"/i.txt")
    for afbeeldingNaam in infoFile.readlines():
        afbeeldingNaam = afbeeldingNaam.strip('\n')
        print("output/"+opname+"/"+object+"/"+afbeeldingNaam)
        afbeelding = cv2.imread("output/"+opname+"/"+object+"/"+afbeeldingNaam)
        resized = cv2.resize(afbeelding, (128, 256), interpolation = cv2.INTER_AREA)
        cv2.imwrite("output2/"+str(teller)+"_"+str(objectTeller)+".jpg", resized)

        if teller%4 == 0:
            f = open("output2/test.txt", "a+")
        elif teller%5 == 0:
            f = open("output2/query.txt", "a+")
        else:
            f = open("output2/train.txt", "a+")

        f.write(str(objectTeller))
        f.write(" ")
        f.write(str(teller)+"_"+str(objectTeller)+".jpg")
        f.write('\n')
        f.close()

        teller = teller+1
    return teller

def verwerkOpname(opname, zelfde, objectTeller, teller):
    infoFile = open("output/"+opname+"/i.txt")
    for object in infoFile.readlines():
        teller = verwerkObject(opname, object.strip('\n'), teller, objectTeller)
        objectTeller = objectTeller + 1

    return objectTeller, teller

objectTeller = 0
teller=0
opnames, zelfde = leesHoofdinput()
for opname in opnames:
    objectTeller, teller = verwerkOpname(opname, zelfde, objectTeller, teller)
