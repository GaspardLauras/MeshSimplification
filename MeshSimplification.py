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




offName = "OFF/tri_gargoyle.off"
#Extraction des données
mesh = meshio.read(filename=offName,file_format="off")
sommets = mesh.points
faces = mesh.cells[0].data

Q=[]
for points in faces:
    p,pt = planEquation(sommets[points])
    Q.append(p*pt)

Q = np.sum(np.array(Q),axis=0) #Valentin le BOSS
print(Q)


planEquation(sommets[faces[0]])

#plotMesh(sommets,faces,offName)



