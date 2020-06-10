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
    return validPairsIndex
    
