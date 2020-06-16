import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plotScatterMatplot(sommets1, sommets2):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xs=sommets1[:,0],
    ys=sommets1[:,1], 
    zs=sommets1[:,2], 
    c='r',marker='o') 
    ax.scatter(xs=sommets2[:,0],
    ys=sommets2[:,1], 
    zs=sommets2[:,2], 
    c='b',marker='*') 
    plt.show()

def plotScatter(sommets,offName):
    fig = go.Figure(data=[go.Scatter3d(
    x=sommets[:,0], 
    y=sommets[:,1], 
    z=sommets[:,2],
    mode='markers',
    marker=dict(
        size=12,
        color=sommets[:,2],                # set color to an array/list of desired values
        opacity=0.8
    )
    )])
    fig.show()

def plotMesh(sommets,faces,offName):
    """
    Fonction qui permet d'afficher à partir de la matrice des points 
    et des surfaces extraite avec openOFF.py/extractDataFromOFF()
    le Mesh correspondant en utilisant la bibliothèque Plotly.
    """
    #print('Sommets',sommets)
    #print('Faces',faces)

    #Plotly
    fig = go.Figure(data=[
        go.Mesh3d(
            #sommets
            x=sommets[:,0], 
            y=sommets[:,1], 
            z=sommets[:,2],
            #Faces
            i=faces[:,0],
            j=faces[:,1],
            k=faces[:,2]
            #couleur
        )]
    )

    fig.update_layout(scene = dict(
        xaxis = dict(
                gridcolor="white",
                showbackground=True,
                zerolinecolor="black"
            ),
            yaxis = dict(
                gridcolor="white",
                showbackground=True,
                zerolinecolor="black"
            ),
            zaxis = dict(
                gridcolor="white",
                showbackground=True,
                zerolinecolor="black"
            ),
        ),
        template='plotly_dark',
        title=offName  
    )
    fig.show()