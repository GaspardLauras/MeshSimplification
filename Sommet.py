import numpy as np

class Sommet:
    """
    Classe correspondant à chaque sommet du mesh contenant
        - ses coordonnées
        - ses Kp
        - son Q
        - les surfaces passant par ce sommet
    """
    #Peut etre supprimer les Kp et les surfaces

    def __init__(self, coords):
        self.coords = coords
    
    def set_Kp(self,kp):
        self.Kp = kp
        return

    def set_Q(self):
        self.Q = np.zeros((4,4))
        for k in self.Kp:
            self.Q += k
        #print('Q : \n',self.Q)
        return    

    def set_surfaces(self,sufaces):
        self.surfaces = sufaces
        return
