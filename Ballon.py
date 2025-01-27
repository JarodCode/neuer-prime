import cv2

class Ballon :
    def __init__(self, sprite, idPos, pos, traj, rayon, enContactGant):

        self.sprite = sprite
        self.idPos = idPos
        self.pos = pos
        self.traj = traj
        self.rayon = rayon
        self.enContactGant = enContactGant
        self.initial_img = cv2.imread(self.sprite, cv2.IMREAD_UNCHANGED)
        self.img = self.initial_img

    #rafraichi l'image si la balle est en l'air, si elle a touché les gants ou si elle est rentrée dans les cages 
    def update(self):
        if not self.enContactGant and self.idPos < self.traj.shape[1] - 1: 
            self.idPos += 1
            self.pos = (int(self.traj[0, self.idPos]), int(self.traj[1, self.idPos]))
            self.initial_img = cv2.rotate(self.initial_img, cv2.ROTATE_90_CLOCKWISE)
            return self.pos
        else: 
            return self.pos
    
    def get_graphic(self):
        return self.img

    def resize_graphic(self, rayon):
        self.img = self.initial_img
        self.rayon = rayon
        self.img = cv2.resize(self.img, (int(rayon), int(rayon)))

    
