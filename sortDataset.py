from PyQt5.QtWidgets import *
import numpy as np
import cv2
import os



class Beschrijf:
    beschrijving = []
    inputFolder = 'output'

    def __init__(self, name):
        self.name = name

    def printBeschrijving(self):
        print("Hoe kan het dier beschreven worden:")
        for b in self.beschrijving:
            print("\t"+ b)

    def addBeschrijving(self, beschrijving):
        self.beschrijving.append(beschrijving)

    def beschrijf(self):
        print("Check de data en beschrijf ze")


        opname = self.__kiesOpname()
        print(opname)
        id = self.__kiesId(opname)
        print(id)

    def __kiesOpname(self):
        opnames = []
        zelfde = []

        #De file lijn per lijn inlezen en de gegevens plaatsen in opnames[] en zelfde[]
        infoFile = open(self.inputFolder+"/info.txt", "r")
        state=0
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

        print("Kies een opname:")
        for i, opname in enumerate(opnames):
            print("\t"+str(i+1)+"\t"+opname)

        print("Geef het nummer in van de genwenste opname:")
        w = int(input())
        return opnames[w-1]

    def __kiesId(self, opname):
        ids = []

        #De file lijn per lijn inlezen en de gegevens plaatsen in opnames[] en zelfde[]
        infoFile = open(self.inputFolder+"/"+opname+"/i.txt", "r")
        for fLine in infoFile.readlines():
            fLine = fLine.strip('\n')
            ids.append(fLine)
        infoFile.close()

        print("Kies een identiteit:")
        for i, id in enumerate(ids):
            print("\t"+str(i+1)+"\t"+id)

        print("Geef het nummer in van het genwenste id:")
        w = int(input())
        return ids[w-1]

    def beschrijfId(self, opname, id):
        #GUI opzetten
        app = QApplication([])

        label = QLabel("Beschrijf " + opname + " -> " + id)
        label.show()

        vbox = QVBoxLayout()
        vbox.setObjectName("Kenmerken")

        vbox.show()


        app.exec_()


beschrijf = Beschrijf("90Graden")
beschrijf.addBeschrijving("vlekKleur")
beschrijf.addBeschrijving("overwegendBevlekt")
beschrijf.printBeschrijving()
beschrijf.beschrijfId("o1", "koe1")


