import numpy as np
import meshio
import copy


def planEquation(threePointsCoords):
    #Fonction renvoyant les équations d'un plan à partir des coordonnées
    #de trois points 
    #Renvois p = [[a],[b],[c],[d]] et pt = [[a,b,c,d]]
    
    p1,p2,p3 = threePointsCoords

    #Calcul des vecteurs v1 = p1p2 et v2 = p1p3
    # Calculer d'abord le np.max p1 p2 p3
    v1 = (p2-p1)/np.max(np.abs(p2-p1))
    v2 = (p3-p1)/np.max(np.abs(p3-p1))
    
    #Calcul de vn = abc avec np.cross 
    vn = np.cross(v1,v2)
    vn = vn/np.linalg.norm(vn)
    a,b,c = vn

    #Calcul de d
    #ax+by+cz+d = 0 => d = -(ax+by+cz)
    d = -(a*p3[0]+b*p3[1]+c*p3[2])

    p = np.array([[a],[b],[c],[d]])
    pt = np.array([[a,b,c,d]])

    """ 
    print('plan : ',a*p3[0]+b*p3[1]+c*p3[2]+d)
    print('plan : ',a*p2[0]+b*p2[1]+c*p2[2]+d)
    print('plan : ',a*p1[0]+b*p1[1]+c*p1[2]+d)
    """
    return p,pt



def get_validPairs(sommets,faces):
    # Fonction renvoyant les indexs des points formant des
    # paires valides à partir d'une liste de points
    # et d'une liste de faces.
    # Cette liste correspond aux arêtes du mesh 
    
    #Liste des paires valides que l'on va remplir et renvoyer
    validPairsIndex = []

    for i in faces: #i correspond à chaque face de la liste faces i=[a b c]
        # On vérifie si [ab] ou [ba] dans la liste des paires valides
        if not ( ([i[0],i[1]] in validPairsIndex) or ([i[1],i[0]] in validPairsIndex) ) :
            validPairsIndex.append([i[0],i[1]])
        
        # On vérifie si [ac] ou [ca] dans la liste des paires valides
        if not ( ([i[0],i[2]] in validPairsIndex) or ([i[2],i[0]] in validPairsIndex) ) :
            validPairsIndex.append([i[0],i[2]])

        # On vérifie si [cb] ou [bc] dans la liste des paires valides
        if not ( ([i[1],i[2]] in validPairsIndex) or ([i[2],i[1]] in validPairsIndex) ) :
            validPairsIndex.append([i[1],i[2]])
    # end for i in faces 
    validPairsIndex = np.array(validPairsIndex)
    return validPairsIndex
    



def get_Points_in_surface(sommets,faces):
    # Fonction renvoyant la liste des surfaces passant par chaque point
    # liste correspondant aux surfaces passant par le point d'indice i:
    # de la forme :
    # [ 'pt0 ' : [0 1 2],[0 2 3],[1 3 4]...
    #   'ptn'  : [...]
    # ] 
    points_in_surface = [[] for i in range(len(sommets))]

    for f in faces: # f = chaque élément de faces (donc chaque face)
        for i in f: # i = chaque indice de sommets dans la face f
            # on ajout à l'emplacement i (correspondant au point #i de sommet) dans points in surface
            # la face f car i est dans f
            points_in_surface[i].append(f)
        # end for i in f:
    # end for f in faces:
    points_in_surface = np.array(points_in_surface)
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
    return Q



def get_deltaVs(sommets,Q):
    deltaVs = []
    for i in range(len(sommets)):
        v = np.concatenate((sommets[i],np.array([1])), axis=0)
        deltaVs.append(v[np.newaxis].T@Q[i]@v)
    deltaVs = np.array(deltaVs)
    return deltaVs



def init(sommets,faces):
    print('IN init')
    points_in_surface = get_Points_in_surface(sommets,faces)
    Kps = get_Kps(sommets,points_in_surface)
    Q = get_Q(Kps)
    validPairsIndex = get_validPairs(sommets, faces)
    print('OUT init')
    return  Q,validPairsIndex



def cost(v,Q):
    vt = np.transpose(v)
    return (vt@Q@v)[0][0]



def gestionFaces(faces, paire):
    v1,v2 = paire
    faces = np.where(faces==v2, v1, faces)
    faces = np.where(faces>=v2, faces-1, faces)
    faces = np.array([face for face in faces if len(np.unique(face)) == len(face)])
    return faces


def gestionValidPairs(paires, paire):
    v1,v2 = paire
    paires = np.where(paires==v2, v1, paires)
    paires = np.where(paires>=v2, paires-1, paires)
    paires = np.array([paire for paire in paires if len(np.unique(paire))==len(paire)])
    return paires



def contraction(sommetsCoords, faces, Q_array,validPairsIndex): 
    sommetsCoords 

    contractedSommets = []
    newDv = []
    newDic = []

    ##################################
    for pair in validPairsIndex:
        Q = Q_array[pair[0]] + Q_array[pair[1]] 
        Qp= [[Q[0][0],Q[0][1],Q[0][2],Q[0][3]],
            [Q[0][1],Q[1][1],Q[1][2],Q[1][3]],
            [Q[0][2],Q[1][2],Q[2][2],Q[2][3]],
            [0      ,0      ,0      ,1      ]]
        Qp = np.array(Qp)

        if np.linalg.det(Qp) > 10**(-4):
            Qp = np.linalg.inv(Qp)
            v = Qp.dot(np.array([[0],[0],[0],[1]]))
        else:
            v= (sommetsCoords[pair[0]] + sommetsCoords[pair[1]])/2
            v= np.transpose(np.concatenate((v,np.array([1.0])), axis=0))
            v = v.reshape((4,1))
        contractedSommets.append(v[0:3])
        Dv = cost(v,Q)
        newDv.append(Dv)
        newDic.append((Dv,v,Q,pair))
    ##################################

    contractedSommets = np.array(contractedSommets)
    newDv = np.array(newDv)
    newDic = sorted(newDic, key=lambda x: x[0])

    minCost, minV, minQ,  minPair = newDic[0]
    
    minPair = sorted(minPair)

    # Gestion des sommets
    sommetsCoords[minPair[0]] = np.transpose(minV[0:3])
    sommetsCoords[minPair[1]] = np.transpose(minV[0:3])
    _,idx = np.unique(sommetsCoords, axis=0, return_index=True)
    idx = np.sort(idx)
    sommetsCoords = sommetsCoords[idx]
    
    # Gestion Faces
    faces = gestionFaces(faces, minPair)

    # Gestion Q
    Q_array[minPair[0]] = minQ
    Q_array = np.delete(Q_array, minPair[1], axis=0)


    # Remplacer et non recaclculer
    print('In validPairs')
    validPairsIndex = gestionValidPairs(validPairsIndex, minPair)
    print('Out validPairs')

    return sommetsCoords,faces,validPairsIndex, Q_array, validPairsIndex


#Ne recalculer que les Q pour les nouveaux points

#Faire deux version 

# Meshs à partir de photos