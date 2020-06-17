import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import meshio
from MeshPlot import *
from SimplificationFonctions import *
from Sommet import Sommet

points = np.array(
    [
        [1,3,1],
        [3,2,2],
        [2,1,3]])
face = np.array([[0,1,2]])
surfaces = get_Points_in_surface(points,face)

#plotMesh(points,face,'tg')

p,pt = planEquation(points)
Kp = p@pt
print('Kp fait à la mano : \n',Kp)

Kps= get_Kps(points,surfaces)
print('Kps : \n',Kps)
