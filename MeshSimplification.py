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
plotMesh(sommets,faces,'AVANT')
sommetsCoords = sommets



################################
validPairsIndex, sommets = init(sommets,faces)

#print('Valid pairs : \n',validPairsIndex)
"""
A TROUVER : QUAND EST-CE QU'ON S'ARRETE?? --> il faut donner un nombre de faces à obtenir à l'avance
"""

contractedSommets = []
newDv = []
newDic = []
for pair in validPairsIndex:
    #print('Pair : ',pair)
    print('-------------')
    Q = sommets[pair[0]].Q + sommets[pair[1]].Q 
    print('Q : \n',Q)
    Qp = [[Q[0][0],Q[0][1],Q[0][2],Q[0][3]],
		  [Q[0][1],Q[1][1],Q[1][2],Q[1][3]],
		  [Q[0][2],Q[1][2],Q[2][2],Q[2][3]],
		  [0      ,0      ,0      ,1      ]]
    Qp = np.array(Qp)
    print('Qp : \n',Qp)
    print('Det : \n',np.linalg.det(Qp))

    if np.linalg.det(Qp) > 10**(-4):
        Qp = np.linalg.inv(Qp)
        v = Qp.dot(np.array([[0],[0],[0],[1]]))
    else:
        v= (sommets[pair[0]].coords + sommets[pair[1]].coords)/2
    
    contractedSommets.append(v[0:3])
    #print('new V : \n',v)
    Dv = cost(v,Q)
    #print('Dv : \n',Dv)
    newDv.append(Dv)
    newDic.append((Dv,v,pair))
    #print('----------')




#print('--------------------------------')
contractedSommets = np.array(contractedSommets)
newDv = np.array(newDv)

newDic = sorted(newDic) #Trie selon le premier élément du tuple
newDic = np.array(newDic)
#print('New dic : \n',newDic)

minCost, minV, minPair = newDic[0]


newSommets = copy.deepcopy(sommetsCoords)

print('sommets not updated : \n',newSommets)
newSommets[minPair[0]] = np.transpose(minV[0:3])
newSommets[minPair[1]] = np.transpose(minV[0:3])
#_,idx = np.unique(newSommets, axis=0, return_index=True)
#idx = np.sort(idx)
#newSommets = newSommets[idx]
print('sommets updated without doublons : \n',newSommets)
#print('Faces : \n',faces)


#plotScatterMatplot(sommetsCoords)
#plot2ScatterMatplot(sommetsCoords,newSommets)
plotMesh(newSommets,faces,'APRES')
################