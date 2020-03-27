from builtins import IOError

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import cv2
import os

class ItterId:
    """Class voor het ittereren over de verschillende identititen in de dataset"""
    #-1 = nog niet geset
    #tuple = waarde
    #0 = klaar
    value = -1

    def __init__(self, inputFolder, debug=0):
        """Functie die alle gegevens inleest om vlot over de identiteiten te kunnen ittereren"""

        self.__inputFolder = inputFolder
        self.__idList = []
        self.__idTeller = 0

        for opname in open(self.__inputFolder + "/info.txt", 'r').readlines():
            opname=opname.strip('\n')
            if opname == "":
                break
            if debug == 1:
                print(opname)
            for id  in open(self.__inputFolder + "/" + opname + "/i.txt", 'r').readlines():
                id = id.strip('\n')
                if debug == 1:
                    print("\t" + id)
                self.__idList.append((opname, id))

    def reset(self):
        """Terug vanaf 0 starten"""
        self.value = -1
        self.__idTeller = 0

    def next(self):
        """Geeft de volgende identiteit.
            Geeft 0 terug wanneer er geen volgende meer is."""

        self.__idTeller += 1
        if self.__idTeller > len(self.__idList):
            self.value = 0
            return self.value
        else:
            self.value = self.__idList[self.__idTeller-1]
            return self.value
    def prev(self):
        """Geeft de vorige identiteit.
            Geeft 0 terug wanneer er geen vorige meer is."""

        self.__idTeller -= 1
        if self.__idTeller == -1:
            self.value = 0
            return self.value
        else:
            self.value = self.__idList[self.__idTeller]
            return self.value

class ToCompare:
    """Class voor het ophalen van te vergelijken classes"""
    #Id's die reeds hetzelfde zijn
    __zelfde = []
    #Id's die reeds vergeleken zijn
    __vergeleken = []

    def __init__(self, inputFolder):
        """Initialiseert de inputfolder var en update zelfde.
        Maakt een basis en vergelijk aan"""
        self.inputFolder = inputFolder
        self.loadZelfde()
        print(self.__zelfde)
        self.loadVergeleken()
        print(self.__vergeleken)
        #Als basis om mee te vergelijken
        self.__basis = ItterId(self.inputFolder)
        self.__basis.next()
        #Hiermee zal altijd worden vergeleken
        self.__vergelijk = ItterId(self.inputFolder)
        self.__vergelijk.next()

        print(self.count())

    def next(self):
        """Volgende vergelijking. Wanneer 0 teruggeven, helemaal rond"""
        if self.__vergelijk.next() != 0:
            #Er is nog een volgende
            if self.done(self.__basis.value, self.__vergelijk.value):
                #Deze moet niet nagekeken worden. Volgende!
                print("Volgende")
                self.__vergelijk.next()
                self.next()
        else:
            #er is er geen meer in deze oname
            if self.__basis.next() == 0:
                return 0
            self.__vergelijk.reset()
            self.__vergelijk.next()

        return 1

    def reset(self):
        self.__basis.reset()
        self.__basis.next()
        self.__vergelijk.reset()
        self.__vergelijk.next()

    def basis(self):
        """Geeft waarde van de basis vergelijking"""
        return self.__basis.value

    def vergelijk(self):
        """Geeft waarde van de te vergelijken id"""
        return self.__vergelijk.value

    def loadZelfde(self):
        """Leest de hoofdinfofile in. Eerst de onpames tot een blanco lijn. Hierna komt de zelfdeinfo"""
        self.__zelfde = []
        #status 0 == opname gegegevens
        #status 1 == zelfde gegevens
        status = 0
        print("Zelfde inlezen...")
        for line in open(self.inputFolder + "/info.txt", "r").readlines():
            line = line.strip('\n')
            if line == "":
                status=1
            elif status == 1:
                line = line.split(" ")
                #Dubbel opslaan om later makkelijk te kunnen zoeken
                self.__zelfde.append([(line[0], line[1]), (line[2], line[3])])
                self.__zelfde.append([(line[2], line[3]), (line[0], line[1])])

    def loadVergeleken(self):
        """Leest de vergeleken file in. In deze file staat beschreven welke identiteiten al vergeleken zijn"""
        self.__vergeleken = []
        try:
            print("Vergelekenfile inlezen:")
            for line in open(self.inputFolder + "/vergeleken.txt", "r").readlines():
                line = line.strip('\n')
                line = line.split(" ")
                print(line)
                #Dubbel opslaan om later makkelijk te kunnen zoeken
                self.__vergeleken.append([(line[0], line[1]), (line[2], line[3])])
                self.__vergeleken.append([(line[2], line[3]), (line[0], line[1])])
        except IOError:
            print("Vergeleken file bestaat nog niet...")
            f = open(self.inputFolder + "/vergeleken.txt", "a+")
            f.close()

    def vergelijkDone(self):
        """Deze combinatie is vergeleken"""
        self.__vergeleken.append([self.__basis.value, self.__vergelijk.value])
        self.__vergeleken.append([self.__vergelijk.value, self.__basis.value])
        self.saveVergeleken()

    def saveVergeleken(self):
        """Slaat een nieuwe versie van de vergeleken file op"""
        try:
            os.remove(self.inputFolder + "/vergeleken.txt")
        except IOError:
            print("Vergelijkenfile bestaat nog niet")
        f = open(self.inputFolder + "/vergeleken.txt", "a+")
        for v in self.__vergeleken:
            if v == [0, 0]:
                break
            f.write(v[0][0] + " " + v[0][1] + " " + v[1][0] + " " + v[1][1])
            f.write('\n')
        f.close()

    def count(self):
        """"Telt hoeveel items nog vergeleken moeten worden.
            Deze functie slaat ook een lijst op van alle identiteiten die vergeleken moeten worden."""

        try:
            os.remove(self.inputFolder + "/teVergelijken.txt")
        except IOError:
            print("teVergelijken bestaat nog niet")

        f = open(self.inputFolder + "/teVergelijken.txt", 'a+')
        aantal = 0

        cBasis = ItterId(self.inputFolder)
        cVergelijk = ItterId(self.inputFolder)
        cVergeleken = []

        while cBasis.next() != 0:
            while cVergelijk.next() != 0:
                #In de lijsten gaan kijken of vergelijken nodig is
                if not self.done(cBasis.value, cVergelijk.value):
                    #Is de virtuele controle al gebeurd tijdens de count?
                    if not self.__inList(cBasis.value, cVergelijk.value, cVergeleken):
                        #Hier moet er normaal visueel gecontroleerd worden
                        f.write(cBasis.value[0]+" "+cBasis.value[1]+" "+cVergelijk.value[0]+" "+cVergelijk.value[1]+"\n")
                        cVergeleken.append([cBasis.value, cVergelijk.value])
                        cVergeleken.append([cVergelijk.value, cBasis.value])
                        aantal += 1
                        print(str(aantal) + " " + str(cBasis.value) + " " + str(cVergelijk.value) + " --- " + str(self.readEigenschappen(cBasis.value)) + " " + str(self.readEigenschappen(cBasis.value)))
            cVergelijk.reset()

        f.close()
        return aantal


    def __inList(self, val1, val2, list):
        """Checkt of een bepaalde combinatie voorkomt in een lijst"""
        for li in list:
            if li[0] == val1:
                if li[1] == val2:
                    return True

        return False

    def done(self, ba, ve):
        """Bekijkt of de combinatie voorkomt in de zelfde in reeds vergeleken lijst"""
        #Niet met jezelf vergelijken
        if ba == ve:
            return True
        #Komen ze uit dezelfde opname?
        if ba[0] == ve[0]:
            return True
        #Zijn ze al aangeduid als zelfde?
        if self.__inList(ba, ve, self.__zelfde):
            return True
        #Zijn ze al visuseel vergeleken?
        if self.__inList(ba, ve, self.__vergeleken):
            return True
        #Bekijken of de eigenschappen hetzelfde zijn, als ze bestaan
        baEigenschappen = self.readEigenschappen(ba)
        veEigenschappen = self.readEigenschappen(ve)
        if self.compEigenschappen(baEigenschappen, veEigenschappen):
            return True

        return False

    def readEigenschappen(self, ba):
        """Geeft een dict terug waarin alle eigenschappen van de id staan"""
        eigenschappen = {}

        try:
            for line in open(self.inputFolder + "/" + ba[0] + "/" + ba[1] + "/beschrijving.txt", 'r').readlines():
                line = line.strip('\n')
                line = line.split("=")
                eigenschappen[line[0]] = line[1]
        except IOError:
            print("Geen beschrijvingsfile")

        return eigenschappen

    def compEigenschappen(self, baEigenschappen, veEigenschappen):
        """De eigenschappen van de twee identiteiten vergelijken en zien of er overeenstemming is.
        Geeft True terug als er een overeenstemming is"""

        for baEigenschap in baEigenschappen:
            if baEigenschap in veEigenschappen:
                if baEigenschappen[baEigenschap] != veEigenschappen[baEigenschap]:
                    return False

        for veEigenschap in veEigenschappen:
            if veEigenschap in baEigenschappen:
                if baEigenschappen[veEigenschap] != veEigenschappen[veEigenschap]:
                    return False

        return True




class LinkDataset:
    """Class voor het linken van de verschillende identiteiten aan zelfde dieren. Een lijst opslaan in info.txt"""

    def __init__(self, inputFolder):
        """Initfunctie die een routinne opstart om de zelfdelijst te vullen.
        Ok zal er bekeken worden hoeveel checks er nog moeten gebeuren."""
        self.inputFolder = inputFolder
        self.__toCompare = ToCompare(self.inputFolder)



link = LinkDataset('output')
