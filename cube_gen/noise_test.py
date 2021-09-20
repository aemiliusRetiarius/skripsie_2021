import numpy as np

import matplotlib.pyplot as plt

mean = 100
percentage = 100

X = np.zeros((100000,))
Y = np.zeros((100000,))

for i in range(100000):
    X[i] = np.random.normal(mean, mean * percentage/100 * 0.28571428)

#plt.plot(X, Y)
plt.hist(X,100)
plt.show()