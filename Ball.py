import cv2

# Ball class represent a football, it has an image which represent it, a position, a radius 
# and a trajectory represented by an array browsed by idPos 

class Ball :
    def __init__(self, sprite, idPos, pos, traj, radius):

        self.sprite = sprite
        self.idPos = idPos
        self.pos = pos
        self.traj = traj
        self.radius = radius
        self.initial_img = cv2.imread(self.sprite, cv2.IMREAD_UNCHANGED)
        self.img = self.initial_img

    # Return the next position of the ball in the trajectory array
    # Also rotate the image by 90°

    def update(self):
        if self.idPos < self.traj.shape[1] - 1: 
            self.idPos += 1
            self.pos = (int(self.traj[0, self.idPos]), int(self.traj[1, self.idPos]))
            self.initial_img = cv2.rotate(self.initial_img, cv2.ROTATE_90_CLOCKWISE)
            return self.pos
        else: 
            return self.pos
        
    # Return the matrix of the ball
    
    def get_graphic(self):
        return self.img
    
    # Change the size of the ball by the radius in argument

    def resize_graphic(self, radius):
        self.img = self.initial_img
        self.radius = radius
        self.img = cv2.resize(self.img, (int(radius), int(radius)))

    
