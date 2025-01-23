import numpy as np
import matplotlib.pyplot as plt 
import scipy as sns

y1 = [0, 500, 200]
x1 = [0, 5, 10]

g = sns.interpolate.CubicSpline(x1, y1)

x2 = np.linspace(0, 10, 500)

y2 = g(x2)

plt.figure(figsize=(10,2))
plt.scatter(x2,y2)
plt.scatter(x1,y1)
plt.show()