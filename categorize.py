from os import listdir
from os import system
from imgdl import read_csv

#Gets the id from the filename which has the format: id.txt
def getID(filename):
    return filename.split('.')[0]
#Directory containing the results.
fileDirectory = "./results/"   
fileList = listdir(fileDirectory)

# get the image ids with their corresponding privacy settings
# id_privacy dictionary has the format - image_id : privacy_setting
ids, id_privacy = read_csv("cleaned.csv");

#file to save the categories
w_f = open("category.txt", 'a')

"""
Format of hte result file:
./train/xxx.jpg: Predicted in xxx.xxx seconds.
object1: xx%
object2: xx%
...
"""
#read each result file and extract objects, then link each object to its privacy setting
for filename in fileList:
    with open("results/" + filename) as r_f:
        for line in r_f:
            if line[0] != '.':
                w_f.write(line.split(':')[0] + " : " + id_privacy[getID(filename)] + "\n")

w_f.close()