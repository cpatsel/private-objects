from os import listdir
from os import system
from copy import deepcopy
import collections
from imgdl import read_csv
import numpy as np
import pandas as pd
import itertools
import math

#Gets the id from the filename which has the format: id.txt
def getID(filename):
    return filename.split('.')[0]

#Directory containing the results.
fileDirectory = "./results/"
fileList = listdir(fileDirectory)

#format -  object : index
object_list = {}

#format - index : object
reversed_object_list = {}

#occurrence - object index : number of occurrence
occurrence = collections.defaultdict(lambda : 0)

# get the image ids with their corresponding privacy settings
# id_privacy dictionary has the format - image_id : privacy_setting
ids, id_privacy = read_csv("cleaned.csv");

"""
Format of hte result file:
./train/xxx.jpg: Predicted in xxx.xxx seconds.
object1: xx%
object2: xx%
...
"""

#assign each object an index
i = 0 #index of objects
for filename in fileList:
    with open("results/" + filename) as r_f:
        for line in r_f:
            if line[0] != '.':
                if (line.split(':')[0]) not in object_list:
                    reversed_object_list[i] = line.split(':')[0]
                    object_list[line.split(':')[0]] = i
                    i += 1

cooccurrency_matrix = [[ x * 0 for x in range(i)] for y in range(i)]
privacy_matrix = [[ x * 0 for x in range(i)] for y in range(i)]

for filename in fileList:
    with open("results/" + filename) as r_f:
        #collect all object indexes in this image, remove duplicates
        objects = set()
        for line in r_f:
            if line[0] != '.':
                # line.split(':')[0] is the object string
                objects.add(object_list[line.split(':')[0]])
        for obj in objects:
            occurrence[obj] += 1
        if len(objects) > 1:
            for i, j in itertools.combinations(objects, 2):
                cooccurrency_matrix[i][j] += 1
                cooccurrency_matrix[j][i] += 1
                if id_privacy[getID(filename)] == "private":
                    privacy_matrix[i][j] -= 1
                    privacy_matrix[j][i] -= 1
                elif id_privacy[getID(filename)] == "public":
                    privacy_matrix[i][j] += 1
                    privacy_matrix[j][i] += 1
#total number of images
n = len(fileList)

# fomular: p(Ci, Cj) * log( p(Ci, Cj) / [ρ(Ci) + ρ(Cj)] )
cooccurrency_socre_matrix = deepcopy(cooccurrency_matrix)
for i in range( len(cooccurrency_socre_matrix) ):
    for j  in range ( len(cooccurrency_socre_matrix[i]) ):
        p_ci_cj = cooccurrency_socre_matrix[i][j] / n
        p_ci = occurrence[i] / n
        p_cj = occurrence[j] / n
        
        if p_ci_cj == 0:
            cooccurrency_socre_matrix[i][j] = 0
        else:
            cooccurrency_socre_matrix[i][j] = p_ci_cj * math.log( p_ci_cj / (p_ci + p_cj) )

def construct_cooccurrency_network():
    i = 0
    j = 0
    data_file = open("network/cooccurrency_adj_list.txt", 'w+')

    for row in cooccurrency_socre_matrix:
        data_line = reversed_object_list[i]
        for item in row:
            if item != 0:
                data_line = data_line + ' ' + reversed_object_list[j]
            j += 1
        i += 1 
        j = 0
        data_line += '\n'
        data_file.write(data_line)

def construct_cooccurrency_gephi():
    node_file = open("network/nodes.csv", 'w+')
    edge_file = open("network/cooccurrency_edges.csv", 'w+')

    node_file.write("id,label\n")
    for k, v in reversed_object_list.items():
        node_file.write(str(k) + "," + v + "\n")
    
    edge_file.write("Source,Target,Type\n")
    #visited = set()
    i = 0
    j = 0
    for row in cooccurrency_socre_matrix:
        for item in row:
            edge_line = str(i) + ','
            if item != 0:
                #if j not in visited:
                    edge_line = edge_line + str(j) + ",Undirected" +'\n'
                    edge_file.write(edge_line)
            j += 1
        #visited.add(i)
        i += 1 
        j = 0

def construct_privacy_gephi():
    edge_file = open("network/privacy_edges.csv", 'w+')
    edge_file.write("Source,Target,Sign,Type\n")

    i = 0
    j = 0
    for row in privacy_matrix:
        for weight in row:
            edge_line = str(i) + ','
            if weight < 0:
                edge_line = edge_line + str(j) + ',' + "0" + ",Undirected" +'\n'
                edge_file.write(edge_line)
            elif weight > 0:
                edge_line = edge_line + str(j) + ',' + "1" + ",Undirected" +'\n'
                edge_file.write(edge_line)
            j += 1
        #visited.add(i)
        i += 1 
        j = 0

construct_cooccurrency_network()
construct_cooccurrency_gephi()
construct_privacy_gephi()

#---------------------------csv files-------------------------------------
names = list(object_list.keys())
df = pd.DataFrame(cooccurrency_socre_matrix, index=names, columns=names)
df.to_csv('matrix/cooccurrency_socre.csv', index=True, header=True, sep=',')

names = list(object_list.keys())
df = pd.DataFrame(cooccurrency_matrix, index=names, columns=names)
df.to_csv('matrix/comatrix.csv', index=True, header=True, sep=',')

names = list(object_list.keys())
df = pd.DataFrame(privacy_matrix, index=names, columns=names)
df.to_csv('matrix/privacy_matrix.csv', index=True, header=True, sep=',')
