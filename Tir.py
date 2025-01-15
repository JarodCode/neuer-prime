import numpy as np

class Tir :

    coDepart = np.array([0, 0, 0])

    def panenka(self):
        coArrivee = np.array([0, 0, -900])          # Remplacer le premier 0 par une valeurs aléatoires entre les valeurs max et le deuxième
        traj = np.zeros([3, 500])                   # ar une valeur aléatoire entre la valeur max - un peu pour viser que le haut et le max
        traj[0, :] = np.linspace(self.coDepart[0], coArrivee[0], traj.shape[1])
        traj[1, :] = np.linspace(self.coDepart[1], coArrivee[1], traj.shape[1])
        traj[1, :] = traj[1, :]**2
        traj[2, :] = np.linspace(self.coDepart[2], coArrivee[2], traj.shape[1])
        return traj

    def direct(self):
        coArrivee = np.array([0, 0, -900])          # Remplacer les 0 par des valeurs aléatoires, prendre en compte le rayon du BALLON
        traj = np.zeros([3, 500])                   # comme c'est coup direct ça peut prendre tout l'écran
        traj[0, :] = np.linspace(self.coDepart[0], coArrivee[0], traj.shape[1])
        traj[1, :] = np.linspace(self.coDepart[1], coArrivee[1], traj.shape[1])
        traj[2, :] = np.linspace(self.coDepart[2], coArrivee[2], traj.shape[1])
        return traj

    def effet(self):
        pass


my_Tir = Tir()

print(my_Tir.direct())
print(my_Tir.panenka())
