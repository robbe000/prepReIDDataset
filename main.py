import numpy as np
import cv2
import os


def genFilenaam(x):
    filenaam = "data/frame_"

    if x < 10:
        filenaam += "00000"
    elif x < 100:
        filenaam += "0000"
    elif x < 1000:
        filenaam += "000"
    elif x < 10000:
        filenaam += "00"
    elif x < 100000:
        filenaam += "0"
    else:
        filenaam += ""

    filenaam += str(x)
    filenaam += ".txt"

    return filenaam

def knip(f, frame, objecten, objctenAantal):
    f1 = f.readlines()
    height, width, channels = frame.shape
    for xi in f1:
        xs = xi.split()
        x = float(xs[1])
        y = float(xs[2])
        w = float(xs[3])
        h = float(xs[4])
        x1 = (x - w/2) * width
        x2 = (x + w/2) * width
        y1 = (y - h/2) * height
        y2 = (y + h/2) * height
        print(str(int(x1))+" "+str(int(x2))+" "+str(int(y1))+" "+str(int(y2)))
        crop_img = frame[int(y1):int(y2), int(x1):int(x2)]
        #cv2.imshow("knipsel", crop_img)
        print("Opslaan...")
        dir = "output/"+objecten[int(xi[0])]
        if objectenAantal[int(xi[0])] == 0:
            if not os.path.exists(dir):
                os.makedirs(dir)
                f1 = open("output/i.txt", "a+")
                f1.write(objecten[int(xi[0])])
                f1.write('\n')
                f1.close()
        cv2.imwrite(dir+"/"+str(objectenAantal[int(xi[0])])+".jpg", crop_img)

        f1 = open(dir+"/i.txt", "a+")
        f1.write(str(objectenAantal[int(xi[0])])+".jpg")
        f1.write('\n')
        f1.close()


        objectenAantal[int(xi[0])] = objectenAantal[int(xi[0])] + 1
    return objectenAantal

#Plaats de Yolo annotatie file in
#Plaats de video file in de data folder en noem hem video.avi
print("Gestart...")

print("Object file lezen...")
fObjects = open("data/obj.names", "r")
fObjectsLines = fObjects.readlines()

objecten = []
objectenAantal = []
for line in fObjectsLines:
    print(line)
    objecten.append(line.strip('\n'))
    objectenAantal.append(0)

fObjects.close()

print("Video inlezen...")
cap = cv2.VideoCapture("data/video.avi")

frameTeller = 0
while cap.isOpened():
    ret, frame = cap.read()
    try:
        f = open(genFilenaam(frameTeller))
        print('Knippen...')
        objectenAantal = knip(f, frame, objecten, objectenAantal)
        f.close()
    except IOError:
        print(str(frameTeller) + " Niets in dit frame")

    cv2.imshow('frame', frame)
    frameTeller = frameTeller + 1
    #cv2.waitKey(1)

cap.release()
cv2.destroyWindow()

teller=0
for o in objecten:
    print(objecten+" "+ str(objectenAantal[teller]))
    teller +=1
