import numpy as np
import scipy as sns
from screeninfo import get_monitors

# Get monitor size to define differents positions 

monitor = get_monitors()[0]
screen_width = monitor.width 
screen_height = monitor.height

# Define global variable

WIDTH, HEIGHT = screen_width, screen_height
MIDW, MIDH = WIDTH/2, HEIGHT/2
WIDTHR, HEIGHTR = WIDTH - 50, HEIGHT - 50
RADIUS = 100
traj = np.zeros([3, 25])

# Shoot class represent all type of trajectory the ball can have,
# direct is a straight shoot that can land anywhere on the screen
# panenka is a shoot that goes in the air and land in the upper part of the screen
# effect is a shoot with a curve that can land in the left or right part of the screen

class Shoot :

    def __init__(self):
        self.traj = traj

    coStart = np.array([MIDW, MIDH + 100])

    # Return an array that represent a trajectory
    # This trajectory is a straight line between start and end points

    def direct(self):
        coStartDirect = np.array([np.random.uniform(RADIUS, WIDTHR), np.random.uniform(RADIUS, HEIGHTR)])
 
        traj[0, :] = np.linspace(self.coStart[0], coStartDirect[0], traj.shape[1])
        traj[1, :] = np.linspace(self.coStart[1], coStartDirect[1], traj.shape[1])

        self.traj = traj

    # Return an array that represent a trajectory
    # This trajectory is the result of the cubic interpolation of the starting, ending and a third points
    # the third point x co is the middle of the segment between the 2 points 
    # the y co is chosen randomly in (-500, -400)

    def panenkaRight(self):
        coEndPanenka = np.array([np.random.uniform(MIDW , WIDTHR), np.random.uniform(RADIUS, RADIUS+50)])
        
        interpX = [self.coStart[0], (self.coStart[0] + coEndPanenka[0])/2, coEndPanenka[0]]
        interpY = [self.coStart[1], -np.random.uniform(400, 500), coEndPanenka[1]]
        interp = sns.interpolate.CubicSpline(interpX, interpY)
        
        traj[0, :] = np.linspace(self.coStart[0], coEndPanenka[0], traj.shape[1])
        traj[1, :] = interp(traj[0, :])

        self.traj = traj


    def panenkaLeft(self):
        coEndPanenka = np.array([np.random.uniform(MIDW , WIDTHR), np.random.uniform(RADIUS, RADIUS+50)])
        
        interpX = [self.coStart[0], (self.coStart[0] + coEndPanenka[0])/2, coEndPanenka[0]]
        interpY = [self.coStart[1], -np.random.uniform(400, 500), coEndPanenka[1]]
        interp = sns.interpolate.CubicSpline(interpX, interpY)
        
        traj[0, :] = np.linspace(self.coStart[0], coEndPanenka[0] - MIDW + RADIUS, traj.shape[1])
        traj[1, :] = interp(np.linspace(self.coStart[0], coEndPanenka[0], traj.shape[1]))

        self.traj = traj

    def panenka(self):
        al = np.random.choice([1,2]) 
        if al == 1 :
            self.panenkaLeft()
        else :
            self.panenkaRight()

    # Return an array that represent a trajectory
    # This trajectory is the result of the cubic interpolation of the starting, ending and a third points
    # the third point x co is the middle of the segment between the 2 points + an int in (95, 105)
    # the third point y co is the middle of the segment between the 2 points + an int in (70, 80)

    def effectLeft(self):
        coEndEffectLeft = np.array([np.random.uniform(WIDTHR - 200 , WIDTHR), np.random.uniform(RADIUS, HEIGHTR)])

        interpX = [self.coStart[0], (self.coStart[0] + coEndEffectLeft[0])/2 + np.random.uniform(95, 105), coEndEffectLeft[0]]
        interpY = [self.coStart[1], (self.coStart[1] + coEndEffectLeft[1])/2 + np.random.uniform(70, 80), coEndEffectLeft[1]]
        interp = sns.interpolate.CubicSpline(interpX, interpY)
        
        traj[0, :] = np.linspace(self.coStart[0], coEndEffectLeft[0] - WIDTHR + 200, traj.shape[1])
        traj[1, :] = interp(np.linspace(self.coStart[0], coEndEffectLeft[0], traj.shape[1])) 

        self.traj = traj



    def effectRight(self):
        coEndEffectRight = np.array([np.random.uniform(WIDTHR - 200 , WIDTHR), np.random.uniform(RADIUS, HEIGHTR)])

        interpX = [self.coStart[0], (self.coStart[0] + coEndEffectRight[0])/2 + np.random.uniform(95, 105), coEndEffectRight[0]]
        interpY = [self.coStart[1], (self.coStart[1] + coEndEffectRight[1])/2 + np.random.uniform(70, 80), coEndEffectRight[1]]
        interp = sns.interpolate.CubicSpline(interpX, interpY)
        
        traj[0, :] = np.linspace(self.coStart[0], coEndEffectRight[0], traj.shape[1])
        traj[1, :] = interp(np.linspace(self.coStart[0], coEndEffectRight[0], traj.shape[1])) 

        self.traj = traj

    def effet(self):
        al = np.random.choice([1,2]) 
        if al == 1 :
            self.effectLeft()
        else :
            self.effectRight()




