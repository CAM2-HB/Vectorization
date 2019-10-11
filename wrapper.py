import os
import sys
import csv

import cv2


def compareSingle(outputPath, dataPath):
	#run openface vectorization on each image in datapath and send output to outputpath
	os.system("../OpenFace/OpenFace/build/bin/FaceLandmarkImg -fdir " + dataPath + " -out_dir " + outputPath)
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


def compareFolder(outputPath, dataPath):
	#run openface vectorization on each image in datapath and send output to outputpath
	for angle in os.listdir(dataPath):
		os.system("../OpenFace/OpenFace/build/bin/FaceLandmarkImg -fdir " + dataPath + angle + " -out_dir " + outputPath + angle)
	for image in os.listdir(outputPath + angle):
		name = image.split('.')
		if len(name) > 1 and name[1] == 'jpg':
			maxconfidence = 0
			maxname = 'Error'
			for folder in os.listdir(outputPath):
				if outputPath + folder + "/" + name[0] + ".csv" in os.listdir(outputPath + folder):
					with open(outputPath + folder + "/" + name[0] + ".csv", 'r') as f:
						data = list(csv.reader(f))
					#confidence in second column, second row of csv
					confidence = float(data[1][1])
					if confidence > maxconfidence:
						maxconfidence = confidence
						maxname = folder
			sys.stdout.write(maxname + " ")
	


if __name__ == "__main__":
	#specify directory that input data is located
	dataPath = "../SampleData/SingleTestIMGs/"
	#specify directory that output will be sent to
	outputPath = "../Output/"
	
	#compareSingle(outputPath, dataPath)
	compareFolder(outputPath, dataPath)
