from os import listdir
from os import system

#Gets the id from the filename, where the filename is of format ID_restof_filename.jpg
def getID(filename):
    return filename.split('_')[0]

#Directory containing the images.
fileDirectory = "./train/"   
fileList = listdir(fileDirectory)

for filename in fileList:
    print(filename)    
    yoloCommand = "./darknet detect cfg/yolov3.cfg yolov3.weights " + fileDirectory+filename  #This will call yolo on the specified image

    fileID = getID(filename)
    yoloCommand = yoloCommand + " > ../results/" + fileID + ".txt" #Redirect output to the results folder. This will contain all the objects predicted to be in this image.
    system(yoloCommand) #Send the command to the shell.

