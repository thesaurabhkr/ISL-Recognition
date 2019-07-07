##Importing the required libraries
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2

##The directory in which the datasets are located
DATADIR = "/root/Saurabh/Jupyter/Project/Dataset"

##The CATEGORIES contains all the different signs present in our dataset
CATEGORIES = ["ABOVE", "ACROSS", "ADVANCE", "ABOARD", "AFRAID", "ALL", "ALONE", "ARISE", "BAG", "BRING",  "ASCEND", "FLAG", "MIDDLE"]

##Each sign contains 6 sets of data
SETS = ["set1", "set2", "set3", "set4", "set5", "set6"]

calculatedValues = np.zeros((200, 6, 36))

##The dimensions of each image
length = 160
breadth = 120

counter1 = 0
counter2 = 0
PI = 3.14159265359
last = 0
for category in CATEGORIES:
    path = os.path.join(DATADIR, category)
    counter2 = 0
    for sets in SETS:
        path2 = os.path.join(path, sets)
        histo = [0.0 for x in range(36)]
        sz = 0
        last = 0
        for img in os.listdir(path2):
            last = last + 1
            sz = sz + 1
            img_array = cv2.imread(os.path.join(path2, img))
            
            ##Converting to gray scale
            gray_array = cv2.imread(os.path.join(path2, img), cv2.IMREAD_GRAYSCALE) 
            
            new_array = cv2.resize(gray_array, (length, breadth))
            
            ##Normalizing the array
            new_array = new_array / 255.0;
            
            du = [[0 for x in range(length)] for y in range(breadth)]
            dv = [[0 for x in range(length)] for y in range(breadth)]
            dist = [[0 for x in range(length)] for y in range(breadth)]
            ang = [[0.0 for x in range(length)] for y in range(breadth)]
            
            for i in range(120):
                for j in range(1, 158):
                    du[i][j+1] = new_array[i][j+2] - new_array[i][j]

            for i in range(160):
                for j in range(1, 118):
                    dv[j+1][i] = new_array[j+2][i] - new_array[j][i]

            import math
            for i in range(120):
                for j in range(160):
                    dist[i][j] = math.sqrt(du[i][j]*du[i][j] + dv[i][j]*dv[i][j])
                    if du[i][j] > 0.0:
                        theta = (180 / PI) * math.atan2(dv[i][j],du[i][j])
                        if theta < 0.0:
                            ang[i][j] = 360.0 + theta
                        else:
                            ang[i][j] = theta

            for i in range(120):
                for j in range(160):
                    tmp = ang[i][j]
                    tmp = tmp / 10.0
                    histo[int(tmp)] = histo[int(tmp)] + dist[i][j]
                    
        tmp = sz * (length * breadth)
        for i in range(36):
            histo[i] = histo[i] / tmp
        
        for i in range(36):
            calculatedValues[counter1][counter2][i] = histo[i]
            
        counter2 = counter2 + 1
    counter1 = counter1 + 1

TESTDIR = "/root/Saurabh/Jupyter/Project/TEST"
histotmp = [0.0 for x in range(36)]
sz = 0
for img in os.listdir(TESTDIR):
    sz = sz + 1
    img_array = cv2.imread(os.path.join(TESTDIR, img))

    ##Converting to gray scale
    gray_array = cv2.imread(os.path.join(TESTDIR, img), cv2.IMREAD_GRAYSCALE) 
    new_array = cv2.resize(gray_array, (length, breadth))

    ##Normalizing the array
    new_array = new_array / 255.0;

    du = [[0 for x in range(length)] for y in range(breadth)]
    dv = [[0 for x in range(length)] for y in range(breadth)]
    dist = [[0 for x in range(length)] for y in range(breadth)]
    ang = [[0.0 for x in range(length)] for y in range(breadth)]

    for i in range(120):
        for j in range(1, 158):
            du[i][j+1] = new_array[i][j+2] - new_array[i][j]

    for i in range(160):
        for j in range(1, 118):
            dv[j+1][i] = new_array[j+2][i] - new_array[j][i]

    import math
    for i in range(120):
        for j in range(160):
            dist[i][j] = math.sqrt(du[i][j]*du[i][j] + dv[i][j]*dv[i][j])
            if du[i][j] > 0.0:
                theta = (180 / PI) * math.atan2(dv[i][j],du[i][j])
                if theta < 0.0:
                    ang[i][j] = 360.0 + theta
                else:
                    ang[i][j] = theta

    for i in range(120):
        for j in range(160):
            tmp = ang[i][j]
            tmp = tmp / 10.0
            histotmp[int(tmp)] = histotmp[int(tmp)] + dist[i][j]

tmp = sz * (length * breadth)
for i in range(36):
    histotmp[i] = histotmp[i] / tmp
    
minimum = 1000000000
minimumindex = 0

for i in range(13):
    for j in range(6):
        diff = 0
        for k in range(36):
            diff = diff + (histotmp[k] - calculatedValues[i][j][k]) * (histotmp[k] - calculatedValues[i][j][k])        if diff < minimum:
            minimum = diff
            minimumindex = i
            
print(minimumindex)
print(CATEGORIES[minimumindex])
