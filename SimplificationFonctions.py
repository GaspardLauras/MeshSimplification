import numpy as np

def planEquation(threePointsCoords): #
    """
    Fonction qui renvoie l'équation du plan défini par les trois points en 
    paramètre sous la forme ax+by+cz+d=0
    P1,P2,P3 vecteurs numpy np.array([x,y,z]) représentant les coordonnées des
    trois points délimitant la surface et donc le plan.
    """
    p1,p2,p3 = threePointsCoords
    v1 = p2-p1
    v2 = p3-p1 
    
    #prendre le max de p1-p2 =m
    #Si m < 1 alors on multiplie par l'inverse de m
    """
    remplacer la fonction cross dans planEquation()par une fonction faite maison
    """
    vn = np.cross(v1/np.linalg.norm(v1),v2/np.linalg.norm(v2))
    
    a,b,c = vn
    #print('a b c :',a,b,c)
    vn = vn/np.sqrt(a**2+b**2+c**2)
    d = np.dot(vn, p3)
    #print('{0}x+{1}y+{2}z+{3}'.format(a,b,c,d))

    p = np.array([[a],[b],[c],[d]])
    pt = np.array([[a,b,c,d]])
    #print('p : ',p)
    #print('pt : ',pt)
    #print('Kp : \n',p*pt)
    #print('------------')
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

def get_Kps(faces,points_in_surface):
    Kps = []
    for i in range(len(points_in_surface)) :
        surface_liste = points_in_surface[i]
        Kpi = []
        for surface in surface_liste:
            p,pt = planEquation(faces[surface])
            Kp = np.dot(p,pt)
            Kpi.append(np.array(Kp))
        Kps.append(np.array(Kpi))
    Kps = np.array(Kps)
    #print('Kps : \n',Kps)
    #print('________________________')
    return Kps

def get_Kps_debug(faces,points_in_surface):
    Kps = []
    Qs = []
    for i in range(len(points_in_surface)) :
        surface_liste = points_in_surface[i]
        Kpi = []
        Q = np.zeros((4,4))
        for surface in surface_liste:
            p,pt = planEquation(faces[surface])
            Kp = np.dot(p,pt)
            Q = Q+Kp
            Kpi.append(np.array(Kp))
        Qs.append(Q)
        Kps.append(np.array(Kpi))
    Kps = np.array(Kps)
    Qs = np.array(Qs)
    #print('Kps : \n',Kps)
    #print('________________________')
    return Kps,Qs

def get_Q(Kps):
    Q = []
    for i in Kps:
        #print(i)
        Q.append(np.sum(i, axis=0))
    Q = np.array(Q)
    #print('Q : \n', Q)
    #print('________________________')
    return Q

def get_deltaVs(sommets,Q):
    deltaVs = []
    for i in range(len(sommets)):
        v = np.concatenate((sommets[i],np.array([1])), axis=0)
        deltaVs.append(v[np.newaxis].T*Q[i]*v)
    deltaVs = np.array(deltaVs)
    #print('Deltas V : \n',deltaVs)
    #print('________________________')
    return deltaVs

