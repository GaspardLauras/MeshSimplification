import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import meshio
from MeshPlot import *
from SimplificationFonctions import *
from Sommet import Sommet
import copy






offName = "sphere"




#########################################
#       Extraction des données:         #
#########################################
mesh = meshio.read(filename="OFF/"+offName+".off",file_format="off")
sommets = mesh.points
sommetsInit = copy.deepcopy(sommets)

faces = mesh.cells[0].data
facesInit = copy.deepcopy(faces)

while len(faces)>50:
    sommets, faces, aretes = contraction(sommets, faces)

#########################################
#        Ecriture des données:          #
#########################################
cells=[('triangle',faces)]
result = meshio.Mesh(sommets,cells)
meshio.write("OFF_results/result_"+offName+".obj",result)



plot(sommets, aretes)