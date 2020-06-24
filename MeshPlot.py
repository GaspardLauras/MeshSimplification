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



    
def lines(points, aretes):
    glBegin(GL_LINES)
    for arete in aretes:
        for p in arete:
            glVertex3fv(points[p])
    glEnd()

def plot(sommets, aretes):


    pg.init()
    display = (1680, 1050)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        glRotatef(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        lines(sommets, aretes)
        pg.display.flip()
        pg.time.wait(10)

