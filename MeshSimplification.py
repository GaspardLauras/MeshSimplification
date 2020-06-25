import numpy as np
import meshio
from SimplificationFonctions import *
from Sommet import Sommet
import copy

import pygame 
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

#Nom du fichier à simplifier
offName = "sphere.off"

#Nombre de faces à atteindre pour arrêter la boucle de simplification
nfaces = 20

def plot_lines(sommets, aretes):
    #Fonction affichant les aretes du mesh
    glColor3d(1,1,1)
    glBegin(GL_LINES)
    for arete in aretes:
        for p in arete:
            glVertex3fv(sommets[p])
    glEnd()

def plot_faces(sommets, faces):
    #Fonction affichant les faces du mesh
    glColor3d(0.25,0.25,0.25)
    glBegin(GL_TRIANGLE_STRIP)
    for face in faces:
        for p in face:
            glVertex3fv(sommets[p])
    glEnd()

#Extraction des données
mesh = meshio.read(filename="OFF/"+offName,file_format="off")

#Sommets
#Liste numpy contenant les coordonées des sommets du mesh
sommets = mesh.points
sommetsInit = copy.deepcopy(sommets)

#Faces
#Numpy contenant les index des points formant une face 
faces = mesh.cells[0].data
facesInit = copy.deepcopy(faces)

#Arêtes
#Numpy contenant les index des sommets formant les aretes 
aretes = get_validPairs(sommetsInit, facesInit)
aretesInit = copy.deepcopy(aretes)

#Init de la fenêtre pygame
pygame.init()
display = (2000,1000)
pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL)
glEnable(GL_DEPTH_TEST)


gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -2*np.max(sommets)-3)

while len(faces)>nfaces or pygame.get_init():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    glRotatef(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    #plot_faces(sommets, faces)
    plot_lines(sommets, aretes)
    pygame.display.flip()
    pygame.time.wait(10)

    #Tant que l'on a pas atteint les n faces voulues
    #On simplifie
    if len(faces)>nfaces:
        sommets, faces, aretes = contraction(sommets, faces)

#Ecriture du résultat dans un fichier
cells=[('triangle',faces)]
result = meshio.Mesh(sommets,cells)
meshio.write("OFF_results/result_"+offName,result)
