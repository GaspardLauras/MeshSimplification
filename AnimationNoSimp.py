import numpy as np
import meshio
from SimplificationFonctions import *
import copy

import pygame 
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time


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



offName = "sphere.off"
saveFile = 'Animations/animation_'+offName.split('.')[0]+'.npy'

data = np.load(saveFile, allow_pickle=True)

#sommets, faces, aretes
sommets = data[:,0]
faces = data[:,1]
aretes = data[:,2]


#Init de la fenêtre pygame
pygame.init()
display = (1500,1000)
pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL)
glEnable(GL_DEPTH_TEST)


gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -2*np.max(sommets[0])-3)

n = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    glRotatef(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    plot_lines(sommets[n], aretes[n])
    pygame.display.flip()
    pygame.time.wait(50)
    n+=1
    if n >= len(sommets):
        n=0