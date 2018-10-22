from os import listdir
from os import system

#Place this file in the directory containing the darknet program.

#Gets the id from the filename, where the filename is of format ID_restof_filename.jpg
def getID(filename):
    return filename.split('_')[0]

fileDirectory = "./train/"   #Directory containing the images.
fileList = listdir(fileDirectory)

for filename in fileList:
    print filename    
    yoloCommand = "./darknet detect cfg/yolov3.cfg yolov3.weights " + fileDirectory+filename  #This will call yolo on the specified image.
    fileID = getID(filename)
    yoloCommand = yoloCommand + " > results/" + fileID + ".txt" #Redirect output to the results folder. This will contain all the objects predicted to be in this image.
    system(yoloCommand) #Send the command to the shell.

