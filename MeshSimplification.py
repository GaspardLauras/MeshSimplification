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
    Kps = get_Kps(sommets,points_in_surface)
    #print('Kps : \n',Kps)
    #Q = get_Q(Kps)
    #deltaVs = get_deltaVs(sommets,Q)
    #print(Q)
    sommetsCLass = []
    for i in range(len(sommets)):
        sommetsCLass.append(Sommet(sommets[i]))
        sommetsCLass[-1].set_Kp(Kps[i])
        sommetsCLass[-1].set_Q()
        sommetsCLass[-1].set_surfaces(points_in_surface[i])
        g = sommetsCLass[-1]
        c = np.concatenate((g.coords, np.array([1])),axis=0)
        #print(c)
        print('cost : ',c@g.Q@c.transpose())
    
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
newDv = []

for pair in validPairsIndex:
    #print('Pair : ',pair)
    Q = sommets[pair[0]].Q + sommets[pair[1]].Q 
    Qp = [[Q[0][0],Q[0][1],Q[0][2],Q[0][3]],
          [Q[0][1],Q[1][1],Q[1][2],Q[1][3]],
          [Q[0][2],Q[1][2],Q[2][2],Q[2][3]],
          [   0   ,   0   ,   0   ,   1   ]]
    Qp = np.array(Qp)
    #print('Qp : \n',Qp)
    print('Det : \n',np.linalg.det(Qp))
    Qp = np.linalg.inv(Qp)
    #print('Qp^-1 : \n',Qp)

    #print('----')
    v = Qp.dot(np.array([[0],[0],[0],[1]]))
    newSommet.append(v[0:3])
    vt = np.transpose(v)
    #print('new V : \n',v)
    #print('new vt : \n',vt)
    Dv = (vt@Q@v)[0][0]
    print('Dv : \n',Dv)
    newDv.append(Dv)
    #print('----------')

"""
Ici on a tous les "points candidats"
Calculer le cout de chaque point candidat D(v) = vT*Q*v
On prend celle qui a le cout le plus faible
Refaire la meme chose avec le nouveau mesh

A TROUVER : QUAND EST-CE QU'ON S'ARRETE?? --> il faut donner un nombre de faces à obtenir à l'avance
"""


#print('--------------------------------')
newSommet = np.array(newSommet)
newDv = np.array(newDv)
#print('New sommets : \n',newSommet)
#print('New Kps : \n',newKps)
print(newSommet[np.argmin(newDv)])
#print(len(newSommet))
plotScatterMatplot(np.array([newSommet[np.argmin(newKps)]]),sommetsCoords)
#plotScatterMatplot(newSommet,sommetsCoords)