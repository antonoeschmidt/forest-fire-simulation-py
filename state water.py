import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))
EMPTY, TREE, FIRE, WATER = 0, 1, 2, 3
colors_list = [(0.2,0,0), (0,0.5,0), (1,0,0), 'orange', 'blue']
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2,3,4]
norm = colors.BoundaryNorm(bounds, cmap.N)

def iterate(X):
	X1 = np.zeros((ny, nx))
	for ix in range(1,nx-1):         
		for iy in range(1,ny-1):            
			if X[iy,ix] == WATER:                 
				X1[iy,ix] = WATER            
			if X[iy,ix] == EMPTY and np.random.random() <= p:                 
				X1[iy,ix] = TREE            
			if X[iy,ix] == TREE:                 
				X1[iy,ix] = TREE                                  
				for dx,dy in neighbourhood:                     
					if X[iy+dy,ix+dx] == FIRE:                         
						X1[iy,ix] = FIRE                         
						break                 
				else:                     
					if np.random.random() <= f:                         
						X1[iy,ix] = FIRE 
                        
		return X1

forest_fraction = 0.2

p, f = 0.05, 0.0001

nx, ny = 100, 100
X  = np.zeros((ny, nx))
X[1:ny-1, 1:nx-1] = np.random.randint(0, 2, size=(ny-2, nx-2))
X[1:ny-1, 1:nx-1] = np.random.random(size=(ny-2, nx-2)) < forest_fraction
X[10:30, 10:12] = WATER
X[30:32, 10:30] = WATER
X[30:60, 30:33] = WATER
X[60:64, 30:88] = WATER

fig = plt.figure(figsize=(25/3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
im = ax.imshow(X, cmap=cmap, norm=norm)
plt.show()