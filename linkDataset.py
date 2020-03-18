from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import cv2
import os

class ItterId:
    """Class voor het ittereren over de verschillende identititen in de dataset"""

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

        print(self.__idList)

    def next(self):
        """Geeft de volgende identiteit.
            Geeft 0 terug wanneer er geen volgende meer is."""

        self.__idTeller += 1
        if self.__idTeller > len(self.__idList):
            return 0
        else:
            return self.__idList[self.__idTeller-1]

    def prev(self):
        """Geeft de vorige identiteit.
            Geeft 0 terug wanneer er geen vorige meer is."""

        self.__idTeller -= 1
        if self.__idTeller == -1:
            return 0
        else:
            return self.__idList[self.__idTeller]


class LinkDataset:
    """Class voor het linken van de verschillende identiteiten aan zelfde dieren. Een lijst opslaan in info.txt"""
    __zelfde = []

    def __init__(self, inputFolder):
        """Initfunctie die een routinne opstart om de zelfdelijst te vullen.
        Ok zal er bekeken worden hoeveel checks er nog moeten gebeuren."""
        self.inputFolder = inputFolder
        self.__leesZelfde()

    def __leesZelfde(self):
        """Leest de hoofdinfofile in. Eerst de onpames tot een blanco lijn. Hierna komt de zelfdeinfo"""
        #status 0 == opname gegegevens
        #status 1 == zelfde gegevens
        status = 0
        for line in open(self.inputFolder + "/info.txt", "r").readlines():
            line = line.strip('\n')
            if line == "":
                status=1
            elif status == 1:
                line = line.split(" ")
                self.__zelfde.append([(line[0], line[1]), (line[2], line[3])])
                self.__zelfde.append([(line[2], line[3]), (line[0], line[1])])

        print(self.__zelfde)
        
link = LinkDataset('output')
