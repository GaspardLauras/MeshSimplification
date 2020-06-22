import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import meshio
from MeshPlot import *
from SimplificationFonctions import *
from Sommet import Sommet
import copy


offName = "OFF/torus5_2.off"

#########################################
#       Extraction des données:         #
#########################################
mesh = meshio.read(filename=offName,file_format="off")
sommets = mesh.points
faces = mesh.cells[0].data
#plotMesh(sommets,faces,offName)
sommetsCoords = sommets

validPairsIndex, sommets = init(sommets,faces)


"""
A TROUVER : QUAND EST-CE QU'ON S'ARRETE?? --> il faut donner un nombre de faces à obtenir à l'avance
"""

contractedSommets = []
newDv = []
newDic = []
for pair in validPairsIndex:
    #print('Pair : ',pair)
    Q = sommets[pair[0]].Q + sommets[pair[1]].Q 
    Qp = [[Q[0][0],Q[0][1],Q[0][2],Q[0][3]],
		  [Q[0][1],Q[1][1],Q[1][2],Q[1][3]],
		  [Q[0][2],Q[1][2],Q[2][2],Q[2][3]],
		  [0      ,0      ,0      ,1      ]]
    Qp = np.array(Qp)
    #print('Qp : \n',Qp)
    #print('Det : \n',np.linalg.det(Qp))
    Qp = np.linalg.inv(Qp)
    #print('Qp^-1 : \n',Qp)

    #print('----')
    v = Qp.dot(np.array([[0],[0],[0],[1]]))
    contractedSommets.append(v[0:3])
    #print('new V : \n',v)
    Dv = cost(v,Q)
    #print('Dv : \n',Dv)
    newDv.append(Dv)
    newDic.append((Dv,v,pair))
    #print('----------')




print('--------------------------------')
contractedSommets = np.array(contractedSommets)
newDv = np.array(newDv)

newDic = sorted(newDic) #Trie selon le premier élément du tuple
newDic = np.array(newDic)
#print('New dic : \n',newDic)

minCost, minV, minPair = newDic[0]


newSommets = copy.deepcopy(sommetsCoords)

#print('sommets not updated : \n',newSommets)
newSommets[minPair[0]] = np.transpose(minV[0:3])
newSommets[minPair[1]] = np.transpose(minV[0:3])
#print('sommets updated : \n',newSommets)
newSommets = np.unique(newSommets, axis=0)
#print('sommets updated without doublons : \n',newSommets)
#print('Faces : \n',faces)


#plotScatterMatplot(sommetsCoords)
plot2ScatterMatplot(sommetsCoords,newSommets)

