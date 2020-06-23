import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import meshio
from MeshPlot import *
from SimplificationFonctions import *
from Sommet import Sommet
import copy


offName = "sphere.off"

#########################################
#       Extraction des données:         #
#########################################
mesh = meshio.read(filename="OFF/"+offName,file_format="off")
sommets = mesh.points
sommetsInit = copy.deepcopy(sommets)
faces = mesh.cells[0].data
plotMesh(sommetsInit,faces,'AVANT')
n_faces = len(faces)
print(n_faces)

""" 
print('Sommets initiaux : \n',sommets)
print('Faces initiales : \n',faces)
print('------------------Début des itérations----------------------') """

i=0
################################
while len(faces)>2:
    i+=1
    sommets, faces = contraction(sommets, faces)
    print('Itération ',i,'\n    ',len(faces))
    
################

print(len(faces))
#plot2ScatterMatplot(sommetsInit,sommets)
plotMesh(sommets,faces,'APRES')

print(sommets)
cells=[('triangle',faces)]

result = meshio.Mesh(sommets,cells)
meshio.write("OFF_results/result_"+offName,result)