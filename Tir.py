import numpy as np
import scipy as sns

# Le gardien se situe en (0, 0, 450)
# Le ballon se situe en (0, 0, -450)

class Tir :

    def __init__(self):
        self.traj = np.zeros([2, 50])

    coDepart = np.array([500, 550, -450])

    def panenkaDroite(self):
        coArriveePanenka = np.array([np.random.uniform(500 , 950), np.random.uniform(50, 200), 450])          # Remplacer le premier 0 par une valeurs aléatoires entre les valeurs max et le deuxième
        
        interpX = [self.coDepart[0], (self.coDepart[0] + coArriveePanenka[0])/2, coArriveePanenka[0]]
        interpY = [self.coDepart[1], -np.random.uniform(500, 600), coArriveePanenka[1]]      # Remplacer 200 par une valeure aléatoire cohérente (faire test)
        interp = sns.interpolate.CubicSpline(interpX, interpY)
        
        traj = np.zeros([3, 50])                   # ar une valeur aléatoire entre la valeur max - un peu pour viser que le haut et le max
        traj[0, :] = np.linspace(self.coDepart[0], coArriveePanenka[0], traj.shape[1])
        traj[1, :] = interp(traj[0, :])
        traj[2, :] = np.linspace(self.coDepart[2], coArriveePanenka[2], traj.shape[1]) #surement changer ca pour que ça soit juste une valeure scalaire(entre 1 et 2 par exemple et augmenter à chaque fois faut voir)

        self.traj = traj

    def direct(self):
        coArriveeDirect = np.array([np.random.uniform(55, 945), np.random.uniform(55, 545)])          # Remplacer les 0 par des valeurs aléatoires, prendre en compte le rayon du BALLON
        traj = np.zeros([2, 50])                   # comme c'est coup direct ça peut prendre tout l'écran
        traj[0, :] = np.linspace(self.coDepart[0], coArriveeDirect[0], traj.shape[1])
        traj[1, :] = np.linspace(self.coDepart[1], coArriveeDirect[1], traj.shape[1])
        # traj[2, :] = np.linspace(self.coDepart[2], coArriveeDirect[2], traj.shape[1])

        self.traj = traj

    def effetGauche(self):
        coArriveeEffetGauche = np.array([0, 0, -450])       # Remplacer les zéros pour que ca prennent des valeurs aléatoires sur les côtés du but

        interpX1 = [self.coDepart[2], (self.coDepart[2] + coArriveeEffetGauche[2])/2, coArriveeEffetGauche[2]]
        interpY1 = [self.coDepart[1], 50, coArriveeEffetGauche[1]]      # Remplacer 200 par une valeure aléatoire cohérente (faire test)
        interp1 = sns.interpolate.CubicSpline(interpX1, interpY1)

        interpX2 = [self.coDepart[2], (self.coDepart[2] + coArriveeEffetGauche[2])/2, coArriveeEffetGauche[2]]
        interpY2 = [self.coDepart[0], -50, coArriveeEffetGauche[0]]      # Remplacer 200 par une valeure aléatoire cohérente (faire test)
        interp2 = sns.interpolate.CubicSpline(interpX2, interpY2)

        traj = np.zeros([3, 500])
        traj[0, :] = np.linspace(self.coDepart[0], coArriveeEffetGauche[0], traj.shape[1])
        traj[0, :] = interp2(traj[0, :])
        traj[1, :] = np.linspace(self.coDepart[1], coArriveeEffetGauche[1], traj.shape[1])
        traj[1, :] = interp1(traj[1, :])
        traj[2, :] = np.linspace(self.coDepart[2], coArriveeEffetGauche[2], traj.shape[1])

        self.traj = traj

    def effetDroite(self):
        coArriveeEffetGauche = np.array([0, 0, -450])       # Remplacer les zéros pour que ca prennent des valeurs aléatoires sur les côtés du but

        interpX1 = [self.coDepart[2], (self.coDepart[2] + coArriveeEffetGauche[2])/2, coArriveeEffetGauche[2]]
        interpY1 = [self.coDepart[1], 50, coArriveeEffetGauche[1]]      # Remplacer 200 par une valeure aléatoire cohérente (faire test)
        interp1 = sns.interpolate.CubicSpline(interpX1, interpY1)

        interpX2 = [self.coDepart[2], (self.coDepart[2] + coArriveeEffetGauche[2])/2, coArriveeEffetGauche[2]]
        interpY2 = [self.coDepart[0], 50, coArriveeEffetGauche[0]]      # Remplacer 200 par une valeure aléatoire cohérente (faire test)
        interp2 = sns.interpolate.CubicSpline(interpX2, interpY2)

        traj = np.zeros([3, 500])
        traj[0, :] = np.linspace(self.coDepart[0], coArriveeEffetGauche[0], traj.shape[1])
        traj[0, :] = interp2(traj[0, :])
        traj[1, :] = np.linspace(self.coDepart[1], coArriveeEffetGauche[1], traj.shape[1])
        traj[1, :] = interp1(traj[1, :])
        traj[2, :] = np.linspace(self.coDepart[2], coArriveeEffetGauche[2], traj.shape[1])

        self.traj = traj




