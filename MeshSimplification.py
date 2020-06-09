import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import meshio
from MeshPlot import plotMesh
from SimplificationFonctions import *
from Sommet import Sommet



offName = "OFF/test.off"

#########################################
#       Extraction des données:         #
#########################################
mesh = meshio.read(filename=offName,file_format="off")
sommets = mesh.points
faces = mesh.cells[0].data
validPairsCoords,validPairsIndex = validPairs(sommets,faces)
""" print("ValidPairsCoords")
print(validPairsCoords)
print("ValidPairsIndex")
print(validPairsIndex)
 """
#########################################
#      Gestion des doublons:         #
#########################################
simplePairsIndex = Pairs(validPairsIndex)
simplePairsCoords = sommets[simplePairsIndex]

#########################################
#   Surfaces passant par chaque point:  #
#########################################
points_in_surface = [[] for i in range(len(sommets))]
for i in range(len(sommets)):
    for j in range(len(faces)):
        if i in faces[j]:
            points_in_surface[i].append(faces[j])
points_in_surface = np.array(points_in_surface)
#print(points_in_surface)


#########################################
#     Calcul de Kp pour chaque point:   #
#########################################
Kps = [[] for i in range(len(sommets))]
for i in range(len(points_in_surface)) :
    surface_liste = points_in_surface[i]
    for surface in surface_liste:
        p,pt = planEquation(faces[surface])
        Kp = p*pt
        Kps[i].append(Kp)
    Kps[i]  = np.array(Kps[i])

#########################################
#     Calcul de Q pour chaque points    #
#########################################
Q = []
for i in Kps:
    #print(i)
    Q.append(np.sum(i, axis=0))
Q = np.array(Q)
#print('Q : \n', Q)


#########################################
#          Calcul de /\(v)              #
#########################################
deltaVs = []
for i in range(len(sommets)):
    v = np.concatenate((sommets[i],np.array([1])), axis=0)
    deltaVs.append(v[np.newaxis].T*Q[i]*v)
deltaVs = np.array(deltaVs)
#print('Deltas V : \n',deltaVs)


#########################################
#            Objets sommets             #
#########################################
sommetsCLass = []
for i in range(len(sommets)):
    sommetsCLass.append(Sommet(sommets[i]))
    sommetsCLass[-1].set_Kp(Kps[i])
    sommetsCLass[-1].set_Q(Q[i])
    sommetsCLass[-1].set_surfaces(points_in_surface[i])
    #print(sommetsCLass[i].__dict__)


#plotMesh(sommets,faces,offName)



