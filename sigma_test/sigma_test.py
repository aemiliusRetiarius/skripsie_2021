from matplotlib import pyplot as mp
import numpy as np
import math

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def drawline(x1, x2, above):
    if above: hanchor = 1.05 
    else: hanchor = 0.95
    mp.plot([x1, x2], [hanchor, hanchor], linestyle='dotted', color='black', alpha=0.6)
    mp.plot([x1, x1], [0, hanchor+0.05], linestyle='dotted', color='black', alpha=0.6)
    mp.plot([x2, x2], [0, hanchor+0.05], linestyle='dotted', color='black', alpha=0.6)
    
    mp.annotate("d ="+str(abs(x1-x2)), (x1+abs(x1-x2)/2, hanchor+0.01), ha='center')

x_axis = np.arange(-5, 15, 0.001)
#mp.plot(x_axis, gaussian(x_axis, 0, math.sqrt(4)), color='blue', label="Initial")
#mp.plot(x_axis, gaussian(x_axis, 10, math.sqrt(4)), color='blue')
#mp.plot(x_axis, gaussian(x_axis, 3.5, math.sqrt(2)), color='red', label="Transformed")
#mp.plot(x_axis, gaussian(x_axis, 6.5, math.sqrt(2)), color='red')
#drawline(3.5, 6.5, False)
#drawline(0.0, 10.0, True)

mp.plot(x_axis, gaussian(x_axis, 0, math.sqrt(0.01)), color='blue', label="Initial")
mp.plot(x_axis, gaussian(x_axis, 10, math.sqrt(0.01)), color='blue')
mp.plot(x_axis, gaussian(x_axis, 2.33, math.sqrt(0.006)), color='red', label="Transformed")
mp.plot(x_axis, gaussian(x_axis, 7.66, math.sqrt(0.006)), color='red')
drawline(2.33, 7.66, False)
drawline(0.0, 10.0, True)

mp.legend()
mp.xlabel("x")
mp.ylabel("p(x)")
mp.show()