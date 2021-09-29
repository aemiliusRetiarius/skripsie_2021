import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import cm
import alphashape as alsh

import subprocess
import os

res_df = pd.read_csv("./result.csv")
print(res_df)
res = np.zeros((98,3))

for i in range(98):
    res[i,0] = res_df["x"][i]
    res[i,1] = res_df["y"][i]
    res[i,2] = res_df["z"][i]

fig = plt.figure()
ax = plt.axes(projection="3d")

ax.scatter3D(res[:, 0], res[:, 1], res[:, 2], c=res[:, 2], cmap='hsv')
plt.show()

#res_list = list(map(tuple, res))
#alpha_shape = alsh.alphashape(res_list, 0.01)
#x.plot_trisurf(*zip(*alpha_shape.vertices), triangles=alpha_shape.faces, cmap=cm.coolwarm)
#plt.show()
