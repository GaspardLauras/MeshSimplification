import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import meshio
from MeshPlot import plotMesh
from SimplificationFonctions import *
from Sommet import Sommet

def init(sommets,faces):
    #########################################
    #        Gestion des doublons:          #
    #########################################
    validPairsIndex = get_validPairs(sommets,faces)
    #print('Valides pairs index : \n',validPairsIndex)
    #print('________________________')


    #########################################
    #   Surfaces passant par chaque point:  #
    #########################################
    points_in_surface = get_Points_in_surface(sommets,faces)

    #########################################
    #     Calcul de Kp pour chaque point:   #
    #########################################
    Kps = get_Kps(faces,points_in_surface)


    #########################################
    #     Calcul de Q pour chaque points    #
    #########################################
    Q = get_Q(Kps)

    #########################################
    #          Calcul de /\(v)              #
    #########################################
    deltaVs = get_deltaVs(sommets,Q)

    #########################################
    #            Objets sommets             #
    #########################################
    sommetsCLass = []
    for i in range(len(sommets)):
        sommetsCLass.append(Sommet(sommets[i]))
        sommetsCLass[-1].set_Kp(Kps[i])
        sommetsCLass[-1].set_Q(Q[i])
        sommetsCLass[-1].set_surfaces(points_in_surface[i])
        #print(sommetsCLass[i].__dict__)
    
    return sommetsCLass

offName = "OFF/test.off"


#########################################
#       Extraction des données:         #
#########################################
mesh = meshio.read(filename=offName,file_format="off")
sommets = mesh.points
faces = mesh.cells[0].data

init(sommets,faces)


#plotMesh(sommets,faces,offName)

