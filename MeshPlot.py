import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from plotly.subplots import make_subplots
import numpy as np

import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def plotMesh(sommets,faces,offName):
    fig = go.Figure(data=[
        go.Mesh3d(
            #sommets
            x=sommets[:,0], 
            y=sommets[:,1], 
            z=sommets[:,2],
            #Faces
            i=faces[:,0],
            j=faces[:,1],
            k=faces[:,2],
            #couleur
            color='cyan',
            opacity=0.50
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



    



