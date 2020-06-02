from MeshPlot import plotMesh
import meshio

offName = "OFF/tri_gargoyle.off"

#Extraction des données
mesh = meshio.read(filename=offName,file_format="off")
sommets = mesh.points
faces = mesh.cells[0].data

plotMesh(sommets,faces,offName)

