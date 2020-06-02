#coding:utf-8
import numpy as np
import pylab as p
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib.tri import Triangulation
import plotly.graph_objects as go
import plotly.express as px



offName = "OFF/cube.off"
    
def extractDataFromOFF(offName):
    offFile = open(offName,'r')
    offData = offFile.readlines()
    offFile.close() 
    """
    offData:line[0] inutile
        * line 1 contient le nombre de sommets
                            nombre de faces
                            nombre de d'arêtes
        * liste de sommets
            
        * List of faces: number of vertices, 
            followed by the indexes of the composing vertices, 
            in order (indexed from zero)
    """
    format = offData[1][0:-1].split(' ')
    sommets=[]
    nSommets = int(format[0])
    faces=[]
    nFaces=int(format[1])

    for i in range (2,nSommets+2):
        sommets.append(offData[i][0:-1].split(' '))
    for i in range(nSommets+3, len(offData)):
        faces.append(offData[i][2:-1].split(' '))


    for i in range (0,len(sommets)):
        print(i, ' : ',sommets[i])
        for j in range (0,3):
            sommets[i][j] = int(sommets[i][j])
    sommets=np.asarray(sommets, dtype=np.float64)
    
    for i in range (0,len(faces)):
        print(i, ' : ',faces[i])
        for j in range (0,3):
            faces[i][j] = int(faces[i][j])
    faces = np.asarray(faces, dtype=np.float64)
    return [sommets,faces]

extractDataFromOFF(offName)


