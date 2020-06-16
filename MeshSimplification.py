import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import meshio
from MeshPlot import *
from SimplificationFonctions import *
from Sommet import Sommet

def init(sommets,faces):
    #Calcul de Q pour tous les sommets initiaux
    points_in_surface = get_Points_in_surface(sommets,faces)
    Kps = get_Kps(faces,points_in_surface)
    Q = get_Q(Kps)
    deltaVs = get_deltaVs(sommets,Q)
    sommetsCLass = []
    for i in range(len(sommets)):
        sommetsCLass.append(Sommet(sommets[i]))
        sommetsCLass[-1].set_Kp(Kps[i])
        sommetsCLass[-1].set_Q(Q[i])
        sommetsCLass[-1].set_surfaces(points_in_surface[i])
    
    #Selection des paires valides
    validPairsIndex = get_validPairs(sommets,faces)

    return validPairsIndex,sommetsCLass

offName = "OFF/test.off"

#########################################
#       Extraction des données:         #
#########################################
mesh = meshio.read(filename=offName,file_format="off")
sommets = mesh.points
faces = mesh.cells[0].data
#plotMesh(sommets,faces,offName)
sommetsCoords = sommets

validPairsIndex, sommets = init(sommets,faces)
#print(sommets)
#print(validPairsIndex)
#print('---------------------------------')

newSommet = []
newKps = []
"""  """
for pair in validPairsIndex:
    Q = sommets[pair[0]].Q + sommets[pair[1]].Q 
    Qp = [[Q[0][0],Q[0][1],Q[0][2],Q[0][3]],
          [Q[0][1],Q[1][1],Q[1][2],Q[1][3]],
          [Q[0][2],Q[1][2],Q[2][2],Q[2][3]],
          [   0   ,   0   ,   0   ,   1   ]]
    Qp = np.array(Qp)
    #print('Qp : \n',Qp)
    #print('Det : \n',np.linalg.det(Qp))
    Qp = np.linalg.inv(Qp)
    #print('Qp^-1 : \n',Qp)

    #print('----')
    v = Qp.dot(np.array([[0],[0],[0],[1]]))
    newSommet.append(v[0:3])
    vt = np.transpose(v)
    print('new V : \n',v)
    print('new vt : \n',vt)
    Dv = vt*Q*v
    print('Dv : \n',Dv)
    print('----------')

"""
Ici on a tous les "points candidats"
Calculer le cout de chaque point candidat D(v) = vT*Q*v
On prend celle qui a le cout le plus faible
Refaire la meme chose avec le nouveau mesh

A TROUVER : QUAND EST-CE QU'ON S'ARRETE??
"""


print('--------------------------------')
newSommet = np.negative(newSommet)
print(np.array(newSommet[0]))
#print(len(newSommet))
#plotScatterMatplot(np.array([newSommet[1]]),sommetsCoords)
