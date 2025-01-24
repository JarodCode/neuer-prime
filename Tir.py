import numpy as np
import scipy as sns

# Le gardien se situe en (0, 0, 450)
# Le ballon se situe en (0, 0, -450)
WIDTH, HEIGHT = 1600, 900
MIDW, MIDH = WIDTH/2, HEIGHT/2
WIDTHR, HEIGHTR = WIDTH - 50, HEIGHT - 50
RAYON = 50

class Tir :

    def __init__(self):
        self.traj = np.zeros([2, 50])

    coDepart = np.array([MIDW, MIDH-100])

    def panenkaDroite(self):
        coArriveePanenka = np.array([np.random.uniform(MIDW , WIDTHR), np.random.uniform(RAYON, RAYON+50)])
        
        interpX = [self.coDepart[0], (self.coDepart[0] + coArriveePanenka[0])/2, coArriveePanenka[0]]
        interpY = [self.coDepart[1], -np.random.uniform(400, 500), coArriveePanenka[1]]
        interp = sns.interpolate.CubicSpline(interpX, interpY)
        
        traj = np.zeros([3, 50])
        traj[0, :] = np.linspace(self.coDepart[0], coArriveePanenka[0], traj.shape[1])
        traj[1, :] = interp(traj[0, :])

        self.traj = traj


    def panenkaGauche(self):
        coArriveePanenka = np.array([np.random.uniform(MIDW , WIDTHR), np.random.uniform(RAYON, RAYON+50)])
        
        interpX = [self.coDepart[0], (self.coDepart[0] + coArriveePanenka[0])/2, coArriveePanenka[0]]
        interpY = [self.coDepart[1], -np.random.uniform(400, 500), coArriveePanenka[1]]
        interp = sns.interpolate.CubicSpline(interpX, interpY)
        
        traj = np.zeros([3, 50])
        traj[0, :] = np.linspace(self.coDepart[0], coArriveePanenka[0] - MIDW + RAYON, traj.shape[1])
        traj[1, :] = interp(np.linspace(self.coDepart[0], coArriveePanenka[0], traj.shape[1]))

        self.traj = traj

    def panenka(self):
        al = np.random.choice([1,2]) 
        if al == 1 :
            self.panenkaGauche()
        else :
            self.panenkaDroite()



    def direct(self):
        coArriveeDirect = np.array([np.random.uniform(RAYON, WIDTHR), np.random.uniform(RAYON, HEIGHTR)])
        traj = np.zeros([2, 25])
        traj[0, :] = np.linspace(self.coDepart[0], coArriveeDirect[0], traj.shape[1])
        traj[1, :] = np.linspace(self.coDepart[1], coArriveeDirect[1], traj.shape[1])

        self.traj = traj



    def effetGauche(self):
        coArriveeEffetGauche = np.array([np.random.uniform(WIDTHR - 200 , WIDTHR), np.random.uniform(RAYON, HEIGHTR)])

        interpX = [self.coDepart[0], (self.coDepart[0] + coArriveeEffetGauche[0])/2 + np.random.uniform(95, 105), coArriveeEffetGauche[0]]
        interpY = [self.coDepart[1], (self.coDepart[1] + coArriveeEffetGauche[1])/2 + np.random.uniform(70, 80), coArriveeEffetGauche[1]]
        interp = sns.interpolate.CubicSpline(interpX, interpY)
        
        traj = np.zeros([3, 25])
        traj[0, :] = np.linspace(self.coDepart[0], coArriveeEffetGauche[0] - WIDTHR + 200, traj.shape[1])
        traj[1, :] = interp(np.linspace(self.coDepart[0], coArriveeEffetGauche[0], traj.shape[1])) 

        self.traj = traj



    def effetDroite(self):
        coArriveeEffetDroite = np.array([np.random.uniform(WIDTHR - 200 , WIDTHR), np.random.uniform(RAYON, HEIGHTR)])

        interpX = [self.coDepart[0], (self.coDepart[0] + coArriveeEffetDroite[0])/2 + np.random.uniform(95, 105), coArriveeEffetDroite[0]]
        interpY = [self.coDepart[1], (self.coDepart[1] + coArriveeEffetDroite[1])/2 + np.random.uniform(70, 80), coArriveeEffetDroite[1]]
        interp = sns.interpolate.CubicSpline(interpX, interpY)
        
        traj = np.zeros([3, 25])
        traj[0, :] = np.linspace(self.coDepart[0], coArriveeEffetDroite[0], traj.shape[1])
        traj[1, :] = interp(np.linspace(self.coDepart[0], coArriveeEffetDroite[0], traj.shape[1])) 

        self.traj = traj

    def effet(self):
        al = np.random.choice([1,2]) 
        if al == 1 :
            self.effetGauche()
        else :
            self.effetDroite()




