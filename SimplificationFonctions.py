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
    
    vn = np.cross(v1,v2)
    a,b,c = vn
    one = a**2+b**2+c**2
    vn = vn/np.sqrt(one)
    d = np.dot(vn, p3)
    #print('{0}x+{1}y+{2}z+{3}'.format(a,b,c,d))

    p = np.array([a,b,c,d])
    pt = p[np.newaxis].T 
    """ print(p)
    print(pt)
    print('Kp : \n',p*pt) """
    return p,pt

def validPairs(sommets,faces):
    validPairsCoords = []
    validPairsIndex = []
    for i in range (len(faces)):
        for j in range (len(faces[i])):
            for j2 in range (len(faces[i])):
                if j != j2:
                    """ print(faces[i][j],faces[i][j2])
                    print(sommets[j],sommets[j2]) """
                    validPairsCoords.append(np.array((sommets[j],sommets[j2])))
                    validPairsIndex.append(np.array((faces[i][j],faces[i][j2])))
    validPairsCoords = np.array(validPairsCoords)
    validPairsIndex = np.array(validPairsIndex)
    return validPairsCoords,validPairsIndex


def Pairs(x):
    new_Pairs = []
    if x is not None:
        for i in x:
            if not ( ([i[0],i[1]] in new_Pairs) or ([i[1],i[0]] in new_Pairs) ) : 
                new_Pairs.append([i[0],i[1]])
    new_Pairs = np.array(new_Pairs)

    return new_Pairs      
