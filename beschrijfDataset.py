from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import cv2
import os

class BeschrijfGuiID:
    def __init__(self, name, opname, id, inputFolder, beschrijvingen, beschrijvingsI, beschrijfClass):
        self.name = name
        self.opname = opname
        self.id = id
        self.inputFolder = inputFolder
        self.beschrijvingen = beschrijvingen
        self.beschrijvingsI = beschrijvingsI
        self.beschrijfClass = beschrijfClass
        self.__afbeeldingen = []
        self.__afbeeldingnr = 0

        #Afbeeldingen inlezen
        pad = self.inputFolder + "/" + self.opname + "/" + self.id
        f = open(pad + "/i.txt")
        for line in f.readlines():
            line = line.strip('\n')
            self.__afbeeldingen.append(pad + "/" + line)

        #De eerste afbeelding weergeven
        self.__afbeeldingWeergeven()

    def __afbeeldingWeergeven(self):
        cv2.imshow("Afbeelding", cv2.imread(self.__afbeeldingen[self.__afbeeldingnr]))
        cv2.moveWindow("Afbeelding", 700, 0)

    def __volgendeAfbeelding(self):
        self.__afbeeldingnr += 1
        if(self.__afbeeldingnr >= len(self.__afbeeldingen)):
            self.__afbeeldingnr = 0

        self.__afbeeldingWeergeven()

    def __vorigeAfbeelding(self):
        self.__afbeeldingnr -= 1
        if(self.__afbeeldingnr < 0):
            self.__afbeeldingnr = len(self.__afbeeldingen)-1

        self.__afbeeldingWeergeven()


    def beschrijfId(self):
        #GUI opzetten
        app = QApplication([])
        self.__IDwindow = QWidget()
        self.__IDwindow.setWindowTitle("Beschrijving")

        #Algemene layout
        v_layout = QVBoxLayout()
        label = QLabel("Beschrijf " + self.opname + " -> " + self.id)
        v_layout.addWidget(label)

        #Groupbox met beschrijvingen
        groupBox = QGroupBox()
        groupBox.setTitle("Kies uit")
        #checkboxen voor in de groupbox
        v_layoutCheckBox = QVBoxLayout()
        self.__inputs = {}
        for beschrijving in self.beschrijvingen:
            v_layoutCheckBox.addWidget(QLabel(beschrijving))
            r = QLineEdit()
            r.setText(self.beschrijvingsI[beschrijving])
            v_layoutCheckBox.addWidget(r)
            self.__inputs[beschrijving] = r
        #Groupbox afwerken
        groupBox.setLayout(v_layoutCheckBox)
        v_layout.addWidget(groupBox)

        #actieknoppen toevoegen
        volgende = QPushButton("Volgende")
        vorige = QPushButton("Vorige")
        sluiten = QPushButton("Sluiten")
        opslaan = QPushButton("Opslaan")
        #Knoppen linken aan layout
        v_layout.addWidget(volgende)
        v_layout.addWidget(vorige)
        v_layout.addWidget(opslaan)
        v_layout.addWidget(sluiten)
        #Knoppen een actie toekennen
        sluiten.clicked.connect(self.__beschrijfIDSluiten)
        opslaan.clicked.connect(self.__beschrijfIDOpslaan)
        volgende.clicked.connect(self.__volgendeAfbeelding)
        vorige.clicked.connect(self.__vorigeAfbeelding)

        #algmene layout toevoegen aan window + weergeven
        self.__IDwindow.setLayout(v_layout)
        self.__IDwindow.show()

        app.exec_()

    def __beschrijfIDSluiten(self):
        print("Idbeschrijver sluiten...")
        self.__IDwindow.close()
        cv2.destroyWindow("Afbeelding")

    def __beschrijfIDOpslaan(self):
        print("Idbeschrijver: gegevens opslaan...")

        #Gegevens uit de GUI ophalen
        for b in self.beschrijvingen:
            self.beschrijvingsI[b] = self.__inputs[b].text()
            print(b + " -> " + self.beschrijvingsI[b])
        self.beschrijfClass.opslaan(self.beschrijvingsI)

        #sluiten
        self.__beschrijfIDSluiten()



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

        afsluiten = 0
        while(afsluiten == 0):
            opname = self.__kiesOpname()
            print(opname)

            terug = 0
            while(terug == 0):
                id = self.__kiesId(opname)
                print(id)

                self.opname = opname
                self.id = id
                self.__beschrijfId()

                print("\nWilt u een andere opname selecteren? [y/N]")
                if(input() == 'y'):
                    terug = 1

            print("\nWilt u stoppen? [y/N]")
            if(input() == 'y'):
                afsluiten = 1



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

    def __beschrijfId(self):
        pad = self.inputFolder + "/" + self.opname + "/" + self.id + "/beschrijving.txt"

        #Bekijken of er al een file bestaat
        #Zo ja, beschrijvingen inlezen en opslaan in beschrijvingsF
        self.__beschrijvingsF = {}
        try:
            f = open(pad)
            for line in f.readlines():
                line = line.strip('\n')
                lineI = line.split('=')
                self.__beschrijvingsF[lineI[0]] = lineI[1]
            f.close()
        except IOError:
            print("Beschrijvingsfile bestaat niet! (" +pad+ ")")

        #De ingelezen waarden vergelijken met de gevraagde beschrijvingen en de info klaarmaken voor de GUI
        beschrijvingsI = {}
        for b in self.beschrijving:
            if b in self.__beschrijvingsF:
                print(b + " gevonden in de beschrijvingsfile!")
                beschrijvingsI[b] = self.__beschrijvingsF[b]
            else:
                beschrijvingsI[b] = ""

        #Gui aanmaken
        gui = BeschrijfGuiID("gui", self.opname, self.id, self.inputFolder, self.beschrijving, beschrijvingsI, self)
        gui.beschrijfId()

    def opslaan(self, beschrijvingsI):
        #De ingegeven waarden aanpassen in de beschrijvingsF dict
        pad = self.inputFolder + "/" + self.opname + "/" + self.id + "/beschrijving.txt"

        for b in self.beschrijving:
            self.__beschrijvingsF[b] = beschrijvingsI[b]

        print(self.__beschrijvingsF)

        try:
            f = open(pad)
            f.close()
            #file verwijderen
            os.remove(pad)
        except IOError:
            print("Beschrijvingsfile bestaat niet! (" +pad+ ")")

        f = open(pad, 'a+')
        for key in self.__beschrijvingsF:
            f.write(key+"="+self.__beschrijvingsF[key])
            f.write("\n")
        f.close()




beschrijf = Beschrijf("90Graden")
beschrijf.addBeschrijving("vlekKleur")
beschrijf.addBeschrijving("overwegendBevlekt")
beschrijf.printBeschrijving()
beschrijf.beschrijf()


