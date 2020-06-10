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
#        Gestion des doublons:          #
#########################################
mesh = meshio.read(filename=offName,file_format="off")
sommets = mesh.points
faces = mesh.cells[0].data
validPairsIndex = validPairs(sommets,faces)
print('Valides pairs index : \n',validPairsIndex)
print('________________________')


#########################################
#   Surfaces passant par chaque point:  #
#########################################
points_in_surface = [[] for i in range(len(sommets))]
for f in faces:
    for i in f:
        points_in_surface[i].append(f)
points_in_surface = np.array(points_in_surface)
print('Points in surfaces : \n',points_in_surface)
print('________________________')


#########################################
#     Calcul de Kp pour chaque point:   #
#########################################
Kps = []
for i in range(len(points_in_surface)) :
    surface_liste = points_in_surface[i]
    Kpi = []
    for surface in surface_liste:
        p,pt = planEquation(faces[surface])
        Kp = p*pt
        Kpi.append(Kp)
    Kps.append(Kp)
Kps = np.array(Kps)
print('Kps : \n',Kps)
print('________________________')


#########################################
#     Calcul de Q pour chaque points    #
#########################################
Q = []
for i in Kps:
    #print(i)
    Q.append(np.sum(i, axis=0))
Q = np.array(Q)
print('Q : \n', Q)
print('________________________')

#########################################
#          Calcul de /\(v)              #
#########################################
deltaVs = []
for i in range(len(sommets)):
    v = np.concatenate((sommets[i],np.array([1])), axis=0)
    deltaVs.append(v[np.newaxis].T*Q[i]*v)
deltaVs = np.array(deltaVs)
#print('Deltas V : \n',deltaVs)
#print('________________________')

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



"""

"""