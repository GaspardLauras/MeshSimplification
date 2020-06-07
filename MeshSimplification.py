import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from MeshPlot import plotMesh
import numpy as np
import meshio

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

    


offName = "OFF/test.off"

#########################################
#       Extraction des données:         #
#########################################
mesh = meshio.read(filename=offName,file_format="off")
sommets = mesh.points
faces = mesh.cells[0].data


#########################################
#   Surfaces passant par chaque point:  #
#########################################
points_in_surface = [[] for i in range(len(sommets))]
for i in range(len(sommets)):
    for j in range(len(faces)):
        if i in faces[j]:
            points_in_surface[i].append(faces[j])
points_in_surface = np.array(points_in_surface)


#########################################
#     Calcul de Kp pour chaque point:   #
#########################################
Kps = [[] for i in range(len(sommets))]
for i in range(len(points_in_surface)) :
    surface_liste = points_in_surface[i]
    for surface in surface_liste:
        p,pt = planEquation(faces[surface])
        Kp = p*pt
        Kps[i].append(Kp)
    Kps[i]  = np.array(Kps[i])


#########################################
#     Calcul de Q pour chaque points    #
#########################################
Q = []
for i in Kps:
    #print(i)
    Q.append(np.sum(i, axis=0))
Q = np.array(Q)
print('Q : \n', Q)


#########################################
#          Calcul de /\(v)              #
#########################################
deltaVs = []
for i in range(len(sommets)):
    v = np.concatenate((sommets[i],np.array([1])), axis=0)
    deltaVs.append(v[np.newaxis].T*Q[i]*v)
deltaVs = np.array(deltaVs)
print('Deltas V : \n',deltaVs)


#plotMesh(sommets,faces,offName)



