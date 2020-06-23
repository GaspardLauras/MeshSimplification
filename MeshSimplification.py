import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import meshio
from MeshPlot import *
from SimplificationFonctions import *
from Sommet import Sommet
import copy


offName = "OFF/sphere.off"

#########################################
#       Extraction des données:         #
#########################################
mesh = meshio.read(filename=offName,file_format="off")
sommets = mesh.points
sommetsInit = copy.deepcopy(sommets)
faces = mesh.cells[0].data
plotMesh(sommetsInit,faces,'AVANT')

""" 
print('Sommets initiaux : \n',sommets)
print('Faces initiales : \n',faces)
print('------------------Début des itérations----------------------') """


################################
for i in range(20):
    sommets, faces = contraction(sommets, faces)
    """ print('Sommets ',i,' : \n',sommets)
    print('Faces ',i,' : \n',faces)
    print('----------------FIN DE L"ITERATION #',i,'----------------------') """
    
################


#plot2ScatterMatplot(sommetsInit,sommets)
plotMesh(sommets,faces,'APRES')