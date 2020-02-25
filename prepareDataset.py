import numpy as np
import cv2
import os

class CreateDataset:
    #Teller die ervoor zorgt dat elke nieuwe identiteit een eigen id krijgt
    __idCounter = 1
    #Folder waarin de inputafbeeldingen zich bevinden.
    #Deze zijn onderverdeeld in verschillende subfolders
    inputFolder = 'output'
    #Folder waarin de de dataset weggeschreven zal worden
    #Ook de train, query en test file komen hierin te staan
    outputFolder = 'output2'
    #Identiteiten die herkend kunnen worden aan opname en naam
    #enlke naam bestaat uit (aantalAfbeeldingen, id, linkId=0)
    opnames = {}


    def __init__(self, name):
        self.name = name

    def __addIdentity(self, opname, identiteit, aantalAfbeeldingen):
        if opname not in self.opnames:
            #de opname bestaat nog niet -> aanmaken
            self.opnames[opname] = {}

        if identiteit not in self.opnames[opname]:
            #de naam bestaat nog niet -> aanmaken
            self.opnames[opname][identiteit] = (aantalAfbeeldingen, self.__idCounter, 0)
            self.__idCounter += 1

        print(self.opnames[opname][identiteit])

    def processIdentities(self):
        state = 0
        opnames = []
        zelfde = []

        #De file lijn per lijn inlezen en de gegevens plaatsen in opnames[] en zelfde[]
        infoFile = open(self.inputFolder+"/info.txt", "r")
        for fLine in infoFile.readlines():
            fLine = fLine.strip('\n')
            if fLine == "":
                state = 1
            else:
                if state == 0:
                    opnames.append(fLine)
                else:
                    zelfde.append(fLine.split())

        infoFile.close()

        #voor alle opnames de juise identiteiten opslaan


dataset = CreateDataset('45Graden')
dataset.processIdentities()
