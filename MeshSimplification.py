import numpy as np
import meshio
from SimplificationFonctions import *
from Sommet import Sommet
import copy

import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


offName = "tore.off"
nfaces = 20

def plot_lines(sommets, aretes):
    glColor3d(1,1,1)
    glBegin(GL_LINES)
    for arete in aretes:
        for p in arete:
            glVertex3fv(sommets[p])
    glEnd()

def plot_faces(sommets, faces):
    glColor3d(0.25,0.25,0.25)
    glBegin(GL_TRIANGLE_STRIP)
    #glVertex3fv(sommets[faces])
    for face in faces:
        for p in face:
            glVertex3fv(sommets[p])
    glEnd()

#Extraction des données
mesh = meshio.read(filename="OFF/"+offName,file_format="off")

#Sommets
sommets = mesh.points
sommetsInit = copy.deepcopy(sommets)

#Faces
faces = mesh.cells[0].data
facesInit = copy.deepcopy(faces)

#Arêtes
aretes = get_validPairs(sommetsInit, facesInit)
aretesInit = copy.deepcopy(aretes)

#Init de la fenêtre pygame
pg.init()
display = (800,900)
pg.display.set_mode(display, pg.DOUBLEBUF|pg.OPENGL)
glEnable(GL_DEPTH_TEST)


gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -2*np.max(sommets)-3)

while len(faces)>nfaces or pg.get_init():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            break
    glRotatef(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    #plot_faces(sommets, faces)
    plot_lines(sommets, aretes)
    pg.display.flip()
    pg.time.wait(10)

    #Tant que l'on a pas atteint les n faces voulues
    #On simplifie
    if len(faces)>nfaces:
        sommets, faces, aretes = contraction(sommets, faces)
        #print(faces)

print('Faces : \n',faces)
#Ecriture du résultat dans un fichier
cells=[('triangle',faces)]
result = meshio.Mesh(sommets,cells)
meshio.write("OFF_results/result_"+offName,result)
