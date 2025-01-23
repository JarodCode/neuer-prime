import numpy as np
import scipy as sns

# Le gardien se situe en (0, 0, 450)
# Le ballon se situe en (0, 0, -450)

class Tir :

    def __init__(self):
        self.traj = np.zeros([2, 50])

    coDepart = np.array([500, 400, -450])

    def panenkaDroite(self):
        coArriveePanenka = np.array([np.random.uniform(500 , 950), np.random.uniform(50, 150), 450])
        
        interpX = [self.coDepart[0], (self.coDepart[0] + coArriveePanenka[0])/2, coArriveePanenka[0]]
        interpY = [self.coDepart[1], -np.random.uniform(500, 600), coArriveePanenka[1]]
        interp = sns.interpolate.CubicSpline(interpX, interpY)
        
        traj = np.zeros([3, 50])
        traj[0, :] = np.linspace(self.coDepart[0], coArriveePanenka[0], traj.shape[1])
        traj[1, :] = interp(traj[0, :])
        traj[2, :] = np.linspace(self.coDepart[2], coArriveePanenka[2], traj.shape[1]) #surement changer ca pour que ça soit juste une valeure scalaire(entre 1 et 2 par exemple et augmenter à chaque fois faut voir)

        self.traj = traj



    def panenkaGauche(self):
        coArriveePanenka = np.array([np.random.uniform(500 , 950), np.random.uniform(50, 150), 450])
        
        interpX = [self.coDepart[0], (self.coDepart[0] + coArriveePanenka[0])/2, coArriveePanenka[0]]
        interpY = [self.coDepart[1], -np.random.uniform(500, 600), coArriveePanenka[1]]
        interp = sns.interpolate.CubicSpline(interpX, interpY)
        
        traj = np.zeros([3, 50])
        traj[0, :] = np.linspace(self.coDepart[0], coArriveePanenka[0] - 450, traj.shape[1])
        traj[1, :] = interp(np.linspace(self.coDepart[0], coArriveePanenka[0], traj.shape[1])) 
        traj[2, :] = np.linspace(self.coDepart[2], coArriveePanenka[2], traj.shape[1]) #surement changer ca pour que ça soit juste une valeure scalaire(entre 1 et 2 par exemple et augmenter à chaque fois faut voir)

        self.traj = traj

    def panenka(self):
        al = np.random.choice([1,2]) 
        if al == 1 :
            self.panenkaGauche()
        else :
            self.panenkaDroite()



    def direct(self):
        coArriveeDirect = np.array([np.random.uniform(55, 945), np.random.uniform(55, 545)])
        traj = np.zeros([2, 25])                   # comme c'est coup direct ça peut prendre tout l'écran
        traj[0, :] = np.linspace(self.coDepart[0], coArriveeDirect[0], traj.shape[1])
        traj[1, :] = np.linspace(self.coDepart[1], coArriveeDirect[1], traj.shape[1])
        # traj[2, :] = np.linspace(self.coDepart[2], coArriveeDirect[2], traj.shape[1])

        self.traj = traj



    def effetGauche(self):
        coArriveeEffetGauche = np.array([np.random.uniform(800 , 950), np.random.uniform(50, 550), 450])       # Remplacer les zéros pour que ca prennent des valeurs aléatoires sur les côtés du but

        interpX = [self.coDepart[0], (self.coDepart[0] + coArriveeEffetGauche[0])/2 + np.random.uniform(45, 55), coArriveeEffetGauche[0]]
        interpY = [self.coDepart[1], (self.coDepart[1] + coArriveeEffetGauche[1])/2 + np.random.uniform(20, 30), coArriveeEffetGauche[1]]
        interp = sns.interpolate.CubicSpline(interpX, interpY)
        
        traj = np.zeros([3, 50])
        traj[0, :] = np.linspace(self.coDepart[0], coArriveeEffetGauche[0] - 750, traj.shape[1])
        traj[1, :] = interp(np.linspace(self.coDepart[0], coArriveeEffetGauche[0], traj.shape[1])) 
        traj[2, :] = np.linspace(self.coDepart[2], coArriveeEffetGauche[2], traj.shape[1]) #surement changer ca pour que ça soit juste une valeure scalaire(entre 1 et 2 par exemple et augmenter à chaque fois faut voir)

        self.traj = traj



    def effetDroite(self):
        coArriveeEffetDroite = np.array([np.random.uniform(800 , 950), np.random.uniform(50, 550), 450])       # Remplacer les zéros pour que ca prennent des valeurs aléatoires sur les côtés du but

        interpX = [self.coDepart[0], (self.coDepart[0] + coArriveeEffetDroite[0])/2 + np.random.uniform(45, 55), coArriveeEffetDroite[0]]
        interpY = [self.coDepart[1], (self.coDepart[1] + coArriveeEffetDroite[1])/2 + np.random.uniform(20, 30), coArriveeEffetDroite[1]]
        interp = sns.interpolate.CubicSpline(interpX, interpY)
        
        traj = np.zeros([3, 50])
        traj[0, :] = np.linspace(self.coDepart[0], coArriveeEffetDroite[0], traj.shape[1])
        traj[1, :] = interp(np.linspace(self.coDepart[0], coArriveeEffetDroite[0], traj.shape[1])) 
        traj[2, :] = np.linspace(self.coDepart[2], coArriveeEffetDroite[2], traj.shape[1]) #surement changer ca pour que ça soit juste une valeure scalaire(entre 1 et 2 par exemple et augmenter à chaque fois faut voir)

        self.traj = traj

    def effet(self):
        al = np.random.choice([1,2]) 
        if al == 1 :
            self.effetGauche()
        else :
            self.effetDroite()




