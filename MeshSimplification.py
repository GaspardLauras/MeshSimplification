import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import meshio
from MeshPlot import *
from SimplificationFonctions import *
from Sommet import Sommet
import copy


offName = "OFF/test.off"

#########################################
#       Extraction des données:         #
#########################################
mesh = meshio.read(filename=offName,file_format="off")
sommets = mesh.points
faces = mesh.cells[0].data
#plotMesh(sommets,faces,'AVANT')




################################
for i in range(20):
    sommets, faces = contraction(sommets, faces)
################


#plot2ScatterMatplot(sommetsCoords,newSommets)
plotMesh(sommets,faces,'APRES')


"""
tests
"""