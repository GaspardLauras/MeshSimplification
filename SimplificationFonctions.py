import numpy as np
from Sommet import Sommet
import meshio
import copy
from MeshPlot import *


def planEquation(threePointsCoords):
    """
    Fonction qui renvoie l'équation du plan défini par les trois points en 
    paramètre sous la forme ax+by+cz+d=0
    P1,P2,P3 vecteurs numpy np.array([x,y,z]) représentant les coordonnées des
    trois points délimitant la surface et donc le plan.
    """
    p1,p2,p3 = threePointsCoords
    """ print('P1 dans planEqution() : \n',p1)
    print('P2 dans planEqution() : \n',p2)
    print('P3 dans planEqution() : \n',p3) """
    v1 = (p2-p1)#/np.abs(np.max(np.abs(p2)-np.abs(p1)))
    v2 = (p3-p1)#/np.abs(np.max(np.abs(p3)-np.abs(p1)))
    #print("v1,v2 : ",v1,v2)
    vn = np.cross(v1,v2)
    vn = vn/np.linalg.norm(vn)
    a,b,c = vn
    #print('a,b,c :',a,b,c)
    d = -(a*p3[0]+b*p3[1]+c*p3[2])
    #print('{0} x + {1} y + {2} z + {3}'.format(a,b,c,d))
    p = np.array([[a],[b],[c],[d]])
    pt = np.array([[a,b,c,d]])
    #print('P : ',p)

    """ print('plan : ',a*p3[0]+b*p3[1]+c*p3[2]+d)
    print('plan : ',a*p2[0]+b*p2[1]+c*p2[2]+d)
    print('plan : ',a*p1[0]+b*p1[1]+c*p1[2]+d) """
    return p,pt

def get_validPairs(sommets,faces):
    #C'est aussi l'oeuvre de Valentin <3
    validPairsIndex = []
    for i in faces:
        if not ( ([i[0],i[1]] in validPairsIndex) or ([i[1],i[0]] in validPairsIndex) ) :
            validPairsIndex.append([i[0],i[1]])

        if not ( ([i[0],i[2]] in validPairsIndex) or ([i[2],i[0]] in validPairsIndex) ) :
            validPairsIndex.append([i[0],i[2]])

        if not ( ([i[1],i[2]] in validPairsIndex) or ([i[2],i[1]] in validPairsIndex) ) :
            validPairsIndex.append([i[1],i[2]])

    validPairsIndex = np.array(validPairsIndex)
    #print('Valides pairs index : \n',validPairsIndex)
    #print('________________________')
    return validPairsIndex
    
def get_Points_in_surface(sommets,faces):
    points_in_surface = [[] for i in range(len(sommets))]
    for f in faces:
        for i in f:
            points_in_surface[i].append(f)
    points_in_surface = np.array(points_in_surface)
    #print('Points in surfaces : \n',points_in_surface)
    #print('________________________')
    return points_in_surface

def get_Kps(sommets,points_in_surface):
    Kps = []
    for i in range(len(points_in_surface)):
        point = points_in_surface[i]
        Kpi = []
        for surface in point:
            p,pt = planEquation(sommets[surface])
            Kpi.append(p@pt)
        Kps.append(np.array(Kpi))
    Kps = np.array(Kps)
    return Kps



def get_Q(Kps):
    Q = np.zeros((np.shape(Kps)[0],4,4))
    for i in range(np.shape(Q)[0]):
        for j in range(np.size(Kps[i],axis=0)):
            Q[i] += Kps[i][j]
    #Q = np.array(Q)
    #print('Q : \n', Q)
    #print('________________________')
    return Q

def get_deltaVs(sommets,Q):
    deltaVs = []
    for i in range(len(sommets)):
        v = np.concatenate((sommets[i],np.array([1])), axis=0)
        deltaVs.append(v[np.newaxis].T@Q[i]@v)
    deltaVs = np.array(deltaVs)
    #print('Deltas V : \n',deltaVs)
    #print('________________________')
    return deltaVs

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
        #print('cost : ',c@g.Q@c.transpose())
    
    #Selection des paires valides
    validPairsIndex = get_validPairs(sommets,faces)

    return validPairsIndex,sommetsCLass

def cost(v,Q):
    #print('v in cost : \n',v)
    vt = np.transpose(v)
    return (vt@Q@v)[0][0]

def contraction(sommets, faces): 
    #prend la liste des sommets et la liste des faces en entrée
    sommetsCoords = sommets
    validPairsIndex, sommets = init(sommets ,faces)
    #print('SommetsCoords : \n',sommetsCoords)
    #print('Valid pairs : \n',validPairsIndex)
    """
    A TROUVER : QUAND EST-CE QU'ON S'ARRETE?? --> il faut donner un nombre de faces à obtenir à l'avance
    """

    contractedSommets = []
    newDv = []
    newDic = []
    for pair in validPairsIndex:
        """ print('-------------')
        print('Pair : ',pair)
        print('Pair coords : \n',sommets[pair[0]].coords ,'\n--\n', sommets[pair[1]].coords)
        print('Pair Qs : \n',sommets[pair[0]].Q ,'\n--\n', sommets[pair[1]].Q) """
        Q = sommets[pair[0]].Q + sommets[pair[1]].Q 
        #print('Q : \n',Q)
        Qp = [[Q[0][0],Q[0][1],Q[0][2],Q[0][3]],
            [Q[0][1],Q[1][1],Q[1][2],Q[1][3]],
            [Q[0][2],Q[1][2],Q[2][2],Q[2][3]],
            [0      ,0      ,0      ,1      ]]
        Qp = np.array(Qp)
        #print('Qp : \n',Qp)
        #print('Det : \n',np.linalg.det(Qp))

        if np.linalg.det(Qp) > 10**(-4):
            Qp = np.linalg.inv(Qp)
            v = Qp.dot(np.array([[0],[0],[0],[1]]))
            #print('det > 10^-4')
        else:
            #print('det <10^-4')
            v= (sommets[pair[0]].coords + sommets[pair[1]].coords)/2
            #print('v in else : \n',type(v[0:3]))
            v= np.transpose(np.concatenate((v,np.array([1.0])), axis=0))
            v = v.reshape((4,1))
        
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
    #print('NewDic : ')
    """ for dic in newDic:
        for truc in dic:
            print(truc)
        print('---') """

    newDic = sorted(newDic, key=lambda x: x[0]) #Trie selon le premier élément du tuple, ici le coût
    #print('New dic : \n',newDic)

    minCost, minV, minPair = newDic[0]


    newSommets = copy.deepcopy(sommetsCoords)

    #print('sommets not updated : \n',newSommets)
    newSommets[minPair[0]] = np.transpose(minV[0:3])
    newSommets[minPair[1]] = np.transpose(minV[0:3])

    _,idx = np.unique(newSommets, axis=0, return_index=True)
    idx = np.sort(idx)
    newSommets = newSommets[idx]
    faces = gestionFaces(faces, minPair)

    #print('sommets updated without doublons : \n',newSommets)
    #print('Faces : \n',faces)

    
    #plotScatterMatplot(newSommets)
    return newSommets,faces

def gestionFaces(faces, paire):
    v1,v2 = sorted(paire)
    #print(v1,v2)

    #print('faces inital : \n',faces)
    faces = np.where(faces==v2, v1, faces)
    #print('faces après suppression du point contracté : \n',faces)

    faces = np.where(faces>=v2, faces-1, faces)
    #print('faces après decrémentation : \n',faces)

    faces = np.array([face for face in faces if len(np.unique(face)) == len(face)])
    #print('faces après gestion des doublons : \n',faces)

    return faces
