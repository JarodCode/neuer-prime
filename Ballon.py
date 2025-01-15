import numpy as np

class Ballon :
    def __init__(self, sprite, idPos, posDebut, posFinal, vitesse, rayon, enContactGant):

        self.sprite = sprite
        self.idPos = idPos
        self.posDebut = posDebut 
        self.posFinal = posFinal
        self.vitesse = vitesse 
        self.rayon = rayon
        self.enContactGant = enContactGant

    #rafraichi l'image si la balle est en l'air, si elle a touché les gants ou si elle est rentrée dans les cages 
    def update(self):
        if not self.enContactGant :
            idPos += 1  
            # Changer le sprite 
        elif self.pos[3] > self.posFinal[3] :
            pass
            # Le but est marqué 
        else :
            pass
            # Le ballon est arrété 

    
