def extractDataFromOFF(offName):
    offData = createReader(offName)
    
    """
    offData:line[0] inutile
        * line 1 contient le nombre de sommets
                            nombre de faces
                            nombre de d'arêtes
        * liste de sommets
            
        * List of faces: number of vertices, 
            followed by the indexes of the composing vertices, 
            in order (indexed from zero)
    """
    print(offData)
    sommets=[]

    faces=[]

    return sommets,faces

def setup():
    offName = "OFF/cube.off"
    offData = createReader(offName)
    
def draw():
    try:
        line = offData.readLine()
    except:
        line = None
        print('Error')
        noLoop()
        
    print(line)
    background(0)
