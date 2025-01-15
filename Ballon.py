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
        if not self.enContactGant :
            self.idPos += 1 
            self.pos = (self.traj[0, self.idPos], self.traj[1, self.idPos], self.traj[2, self.idPos])
            # Changer le sprite 
        elif self.pos[3] > self.posFinal[3] :
            pass
            # Le but est marqué 
        else :
            pass
            # Le ballon est arrété 
    
    def get_graphic(self):
        img = Graphic(cv2.imread(self.sprite, cv2.IMREAD_UNCHANGED))
        img.resize((self.rayon, self.rayon), cv2.INTER_NEAREST)
        return img

    
