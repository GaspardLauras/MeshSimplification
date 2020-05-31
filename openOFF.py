#coding:utf-8
import numpy as np
import pylab as p
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib.tri import Triangulation
import plotly.graph_objects as go
import plotly.express as px



offName = "OFF/bague.off"
    
def extractDataFromOFF(offName):
    offFile = open(offName,'r')
    offData = offFile.readlines()
    offFile.close() 
    print('Off Data',len(offData))
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
    #print(format)
    sommets=[]
    nSommets = int(format[0])
    faces=[]
    nFaces=int(format[1])

    print('Sommets',nSommets)
    print('Faces',nFaces)

    for i in range (2,nSommets+2):
        sommets.append(offData[i][0:-1].split(' '))
        #print(sommets[-1])
    
    for i in range(nSommets+4, nSommets+3+nFaces):
        faces.append(offData[i][0:-1].split(' '))
        #print(faces[-1])

    sommets=np.asarray(sommets, dtype=np.float64)
    #print('Sommets',sommets)
    faces = np.asarray(sommets, dtype=np.float64)
    #print('Faces',faces)
    return sommets,faces

sommets,faces=extractDataFromOFF(offName)
sommets=np.array(sommets)
#print(sommets)
faces = np.array(faces)
#print(faces)


#Plotly
fig = go.Figure(data=[
    go.Scatter3d(
        mode = 'markers',
        x=sommets[:,0], 
        y=sommets[:,1], 
        z=sommets[:,2],
        marker=dict(
            size=2
        )
    )] 
)
fig.update_layout(scene = dict(
    xaxis = dict(
            backgroundcolor="rgb(255,255,255)",
            gridcolor="white",
            showbackground=True,
            zerolinecolor="white",),
    yaxis = dict(
            backgroundcolor="rgb(255,255,255)",
            gridcolor="white",
            showbackground=True,
            zerolinecolor="white",),
    zaxis = dict(
            backgroundcolor="rgb(255,255,255)",
            gridcolor="white",
            showbackground=True,
            zerolinecolor="white",),),
)

#fig.show()


