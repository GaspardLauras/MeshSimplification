import numpy as np
import meshio
from SimplificationFonctions import *

#Nom du fichier à simplifier
offName = "tri_gargoyle.off"

#Nombre de faces à atteindre pour arrêter la boucle de simplification
nfaces = 20

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

Q_array, validPairsIndex = init(sommets, faces)
#print(Q_array)

while len(faces)>nfaces:
    sommets, faces, aretes, Q_array, validPairsIndex = contraction(sommets, faces, Q_array,validPairsIndex)
    print(len(aretes))
    print('-')

print('CONTRACTION DONE')

#Ecriture du résultat dans un fichier
cells=[('triangle',faces)]
result = meshio.Mesh(sommets,cells)
meshio.write("OFF_results/result_"+offName,result)