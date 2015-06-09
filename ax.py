import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

im = np.arange(100)
im.shape = 10, 10

fig = plt.figure(1, (5., 5.))
grid = ImageGrid(fig, (0.1, 0.4, 0.2, 0.2), # similar to subplot(111)
                nrows_ncols = (2, 2), # creates 2x2 grid of 
                share_all = True,
                axes_pad=0.1, # pad between axes in inch.
                )
grid2 = ImageGrid(fig, (0.1, 0.7, 0.2, 0.2), # similar to subplot(111)
                nrows_ncols = (2, 2), # creates 2x2 grid of 
                share_all = True,
                axes_pad=0.1, # pad between axes in inch.
                )
grid3 = ImageGrid(fig, (0.1, 0.1, 0.2, 0.2), # similar to subplot(111)
                nrows_ncols = (2, 2), # creates 2x2 grid of axes
                share_all = True,
                axes_pad=0.1, # pad between axes in inch.
                )

#for i in range(4):
    #grid[i].imshow(im) # The AxesGrid object work as a list of axes.
#for j in range(4):
    #grid2[j].imshow(im) # The AxesGrid object work as a list of axes.
plt.show()
