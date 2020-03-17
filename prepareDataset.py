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
    #enlke naam bestaat uit (id, aantalAfbeeldingen, gelinkt=0)
    opnames = {}
    #Naam van de trainingsfile
    trainFileName = "train.txt"
    #Naam van de queryfile
    queryFileName = "query.txt"
    #Naam van de testfile
    testFileName = "test.txt"
    #Maximaal aantal afbeeldingen per identiteit
    maxPictures = 30
    #Output afbeelding breedte
    outputWidth = 128
    #Output afbeelding hoogte
    outputHeight = 256
    #Het exemplaar dat momenteel zal weggeschreven worden
    __exemplaarNummer = 0
    #Het output id dat zal worden gebruikt door het netwerk. Dit moet 0, 1, 2,... zijn!
    __outputId = {}


    def __init__(self, name):
        self.name = name

    def __addIdentity(self, opname, identiteit, aantalAfbeeldingen):
        if opname not in self.opnames:
            #de opname bestaat nog niet -> aanmaken
            self.opnames[opname] = {}

        if identiteit not in self.opnames[opname]:
            #de naam bestaat nog niet -> aanmaken
            self.opnames[opname][identiteit] = (self.__idCounter, aantalAfbeeldingen, 0)
            self.__idCounter += 1

    def processIdentitiesInfo(self):
        print('Files inlezen en gegevens verwerken...')
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

        #Voor alle opnames de juise identiteiten opslaan (inc aantal afbeeldingen bepalen)
        for opname in opnames:
            opnameFile = open(self.inputFolder+"/"+opname+"/i.txt", "r")
            #Alle identiteiten afgaan in de opnamefile
            for oLine in opnameFile.readlines():
                oLine = oLine.strip('\n')
                #het aantal afbeeldingen bepalen per identiteit
                identiteitFile = open(self.inputFolder+"/"+opname+"/"+oLine+"/i.txt", "r")
                aantalAfbeeldingen = sum(1 for line in identiteitFile)
                identiteitFile.close()
                #De info opslaan in de class
                self.__addIdentity(opname, oLine, aantalAfbeeldingen)

            opnameFile.close()

        print("Checken op zelfde identiteiten")
        self.__checkSame(zelfde)

        print('DONE!\nNu kan de dataset gecreerd worden!')

    def __checkSame(self, zelfde):
        for zelf in zelfde:
            #Het id van de tweede vermelding gelijk maken aan het id van de eerste vermelding
            id1 = self.opnames[zelf[0]][zelf[1]][0]
            aantal = self.opnames[zelf[0]][zelf[1]][1] + self.opnames[zelf[2]][zelf[3]][1]
            #Eerste element aanpassen
            self.opnames[zelf[0]][zelf[1]] = (id1, aantal, 1)
            self.opnames[zelf[2]][zelf[3]] = (id1, aantal, 1)

    def createDataset(self):
        print("WARNING: Zorg ervoor dat er een folder "+self.outputFolder+" bestaat en dat deze folder leeg is. \n\tDruk op enter om verder te gaan.")
        input()

        #Alle opnames doorzoeken en hieruit alle afzonderlijke identiteiten verwerken
        for opname in self.opnames:
            for identiteit in self.opnames[opname]:
                id = self.opnames[opname][identiteit][0]
                aantalAfbeeldingen = self.opnames[opname][identiteit][1]
                print("VERWERK "+opname+"\t"+identiteit+"\t"+str(id)+"\t"+str(aantalAfbeeldingen))
                print("i.txt verwerken...")
                fi = open(self.inputFolder+"/"+opname+"/"+identiteit+"/i.txt", 'r')
                afbeeldingPaden = []
                for iLine in fi.readlines():
                    iLine = iLine.strip('\n')
                    afbeeldingPaden.append(self.inputFolder+"/"+opname+"/"+identiteit+"/"+iLine)
                fi.close()
                self.__processIdentitie(id, aantalAfbeeldingen, afbeeldingPaden)

        print(self.__outputId)

    def __processIdentitie(self, id, aantalAfbeeldingen, afbeeldingPaden):
        #Bepalen welke afbeeldingen bekeken moeten worden aan de hand van het aantal afbeeldingen
        mod = int(aantalAfbeeldingen/self.maxPictures)
        for i, pad in enumerate(afbeeldingPaden):
            if self.maxPictures<aantalAfbeeldingen:
                if i%mod == 0:
                    print(str(i)+"\t"+pad)
                    self.__processImage(id, i, afbeeldingPaden[i], self.__exemplaarNummer)
            else:
                print(str(i)+"\t"+pad+"\tAlles")
                self.__processImage(id, i, afbeeldingPaden[i], self.__exemplaarNummer)
            self.__exemplaarNummer+=1

    def __processImage(self, id, imId, pad, exemplaarNummer):
        image = cv2.imread(pad)
        resized = cv2.resize(image, (self.outputWidth, self.outputHeight), interpolation = cv2.INTER_AREA)
        cv2.imshow("afbeelding", image)
        cv2.imshow("Output Image", resized)
        cv2.waitKey(10)

        outputPad = self.outputFolder+"/"+str(id)+"_"+str(imId)+".jpg"
        cv2.imwrite(outputPad, resized)

        #id omzetten naar outputId
        if id not in self.__outputId:
            #eerste het outputId, dan te teller om de data te verdelen
            self.__outputId[id] = [len(self.__outputId), 0]

        if self.__outputId[id][1] == 6:
            self.__outputId[id][1] = 0

        if self.__outputId[id][1] == 0 | self.__outputId[id][1] == 1:
            f = open(self.outputFolder+"/"+self.testFileName, 'a+')
        elif self.__outputId[id][1] == 2:
            f = open(self.outputFolder+"/"+self.queryFileName, 'a+')
        else:
            f = open(self.outputFolder+"/"+self.trainFileName, 'a+')

        self.__outputId[id][1] += 1

        f.write(str(self.__outputId[id][0]))
        f.write(' ')
        f.write(outputPad)
        f.write('\n')
        f.close()

dataset = CreateDataset('45Graden')
dataset.processIdentitiesInfo()
dataset.createDataset()

print("\n")
print(dataset.opnames)
