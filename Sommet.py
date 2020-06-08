import numpy as np

class Sommet:
    """
    Classe correspondant à chaque sommet du mesh contenant
        - ses coordonnées
        - ses Kp
        - son Q
        - les surfaces passant par ce sommet
    """

    def __init__(self, coords):
        self.coords = coords
    
    def set_Kp(self,kp):
        self.Kp = kp
        return

    def set_Q(self,Q):
        self.Q = Q
        return    

    def set_surfaces(self,sufaces):
        self.surfaces = sufaces
        return
