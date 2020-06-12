import plotly.graph_objects as go
import plotly.express as px
import numpy as np

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