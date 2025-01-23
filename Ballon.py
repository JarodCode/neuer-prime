import numpy as np
from Graphics import Graphic, SceneRender
import cv2
from Tir import Tir

class Ballon :
    def __init__(self, sprite, idPos, pos, traj, rayon, enContactGant):

        self.sprite = sprite
        self.idPos = idPos
        self.pos = pos
        self.traj = traj
        self.rayon = rayon
        self.enContactGant = enContactGant

    #rafraichi l'image si la balle est en l'air, si elle a touché les gants ou si elle est rentrée dans les cages 
    def update(self):
        if not self.enContactGant and self.idPos < self.traj.shape[1] - 1:  # Vérifie si idPos est valide
            self.idPos += 1
            self.pos = (int(self.traj[0, self.idPos]), int(self.traj[1, self.idPos]))
            return self.pos

            # Changer le sprite 
        # elif self.pos[2] > self.posFinal[2] :
        #     pass
        #     print("BUUUUUUT!!!!!!")
        # else :
        #     pass
        #     print("MAIS QUEL ARRET!!!!!") 
    
    def get_graphic(self):
        img = Graphic(cv2.imread(self.sprite, cv2.IMREAD_UNCHANGED))
        img.resize((self.rayon, self.rayon), cv2.INTER_NEAREST)
        return img

    
