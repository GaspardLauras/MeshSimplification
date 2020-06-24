import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import meshio
from MeshPlot import *
from SimplificationFonctions import *
from Sommet import Sommet
import copy







offName = "sphere"




#########################################
#       Extraction des données:         #
#########################################
mesh = meshio.read(filename="OFF/"+offName+".off",file_format="off")
sommets = mesh.points
sommetsInit = copy.deepcopy(sommets)

faces = mesh.cells[0].data
facesInit = copy.deepcopy(faces)

aretes = get_validPairs(sommetsInit, facesInit)
aretesInit = copy.deepcopy(aretes)

pg.init()
display = (1680, 1050)
pg.display.set_mode(display, DOUBLEBUF|OPENGL)

gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

glTranslatef(0.0, 0.0, -5)

while len(faces)>50 or pg.get_init():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    glRotatef(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    lines(sommets, aretes)
    pg.display.flip()
    pg.time.wait(10)
    if len(faces)>50:
        sommets, faces, aretes = contraction(sommets, faces)

#########################################
#        Ecriture des données:          #
#########################################
cells=[('triangle',faces)]
result = meshio.Mesh(sommets,cells)
#meshio.write("OFF_results/result_"+offName+".obj",result)
""" 
plot(sommetsInit, get_validPairs(sommetsInit, facesInit))
plot(sommets, aretes) """