import os
import sys
import csv
import math
import shutil
from itertools import islice
import cv2


def compareSingle(outputPath, dataPath):
    #run openface vectorization on each image in datapath and send output to outputpath
    os.system("..OpenFace/OpenFace/build/bin/FaceLandmarkImg -fdir " + dataPath + " -out_dir " + outputPath)
    maxconfidence = 0
    for item in os.listdir(outputPath):
        name = item.split('.')
        #identify all csvs and find the highest confidence
        if len(name) > 1 and name[1] == 'csv':
            with open(outputPath + item, 'r') as f:
                data = list(csv.reader(f))
            #confidence in second column, second row of csv
            confidence = float(data[1][1])
            if confidence > maxconfidence:
                maxconfidence = confidence
                maxname = name[0]

    #use opencv for analysis on the image associated with the highest confidence and print confidence onto the image and display
    img = cv2.imread(outputPath + maxname + '.jpg')
    cv2.putText(img, str(maxconfidence), (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 2.0, color=(0, 255, 255))
    #displays image
    cv2.imshow('image',img)
    #saves image
    cv2.imwrite('img.jpg', img)
    cv2.waitKey(1000)
    return


def compareFolder(outputPath, dataPath, finalPath):
    #run openface vectorization on each image in datapath and send output to outputpath
    final = []
    for angle in os.listdir(dataPath):
        os.system("../OpenFace/OpenFace/build/bin/FaceLandmarkImg -fdir " + dataPath + angle + " -out_dir " + outputPath + angle)
    #for each timeframe
    for image in os.listdir(outputPath + angle):
        imagedata = []
        name = image.split('.')
        #find jpgs
        if len(name) > 1 and name[1] == 'jpg':
            maxconfidence = 0
            #compare jpgs across folders at each timeframe (img0000 in folder 1, 2, 3)
            for folder in os.listdir(outputPath):
                #check whether it's a folder or not
                if os.path.isdir(outputPath + folder):
                    if name[0] + ".csv" in os.listdir(outputPath + folder):
                        with open(outputPath + folder + "/" + name[0] + ".csv", 'r') as f:
                            data = list(csv.reader(f))
                        #confidence in second column, second row of csv
                        confidence = float(data[1][1])
                        if confidence > maxconfidence:
                            maxconfidence = confidence
                            for index, d in enumerate(data[0]):
				#search top row of CSV for pose_Ry, which is the angle we are analyzing for starters
                                if d == ' pose_Ry':
                                    maxangle = round(math.degrees(float(data[1][index])), 4)
                            maxname = folder

            
            #identifies image with highest confidence at each timeframe and adds it to finalPath, adds image ID, folder, confidence to final text file
#            shutil.copy(outputPath + maxname + '/' + name[0] + '.jpg', finalPath)
            imagedata = [name[0][-4:], maxname, maxconfidence, maxangle]
            final.append(imagedata)
            
            #print confidence onto the final images
            img = cv2.imread(outputPath + maxname + '/' + name[0] + '.jpg')
            
            cv2.putText(img, str(imagedata), (0, len(img) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            #saves image
            write_name = finalPath + '/' + name[0] + '.jpg'
            cv2.imwrite(write_name, img)
            
            
    with open(finalPath + 'final.txt', 'w') as f:
        f.write("image, camera, confidence, angle\n")
        for data in final:
            f.write(data[0] + ", " + data[1] + ", " + str(data[2]) + ", " + str(data[3]) + '\n')
    #sort and print the finaldata
    a = []
    print("image, camera, confidence")
    with open(finalPath + 'final.txt', 'r') as f:
        for line in islice(f, 1, None): #skip the title line
            a.append(line.strip())
        for item in sorted(a):
            print(item)
    print("View final output images and data in " + str(finalPath))
    return
    

if __name__ == "__main__":
    #clear the outputPath and finalPath before running the code
    shutil.rmtree('../Output/')
    os.mkdir('../Output/')
    shutil.rmtree('../Final/Ethan/')
    os.mkdir('../Final/Ethan/')
    
    #specify directory that input data is located
    dataPath = "../SampleData/SingleTestIMGs/"
    #specify directory that output will be sent to
    outputPath = "../Output/"
    finalPath = '../Final/Ethan/'

#    compareSingle(outputPath, dataPath)
    compareFolder(outputPath, dataPath, finalPath)
