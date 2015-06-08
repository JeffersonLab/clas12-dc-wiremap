import time
import numpy as np
from numpy import random as rand
from matplotlib import pyplot, gridspec, animation

data = rand.uniform(0,100,(36,6,112))

fig = pyplot.figure(1, (18,8))
axs = []
pts = []

sector_grid = gridspec.GridSpec(2,3,wspace=0.3,hspace=0.3)
for sec in range(6):
    slyr_grid = gridspec.GridSpecFromSubplotSpec(6,1,
        wspace=0.0,hspace=0.1,
        subplot_spec=sector_grid[sec])

    for slyr in range(6):

        axs += [fig.add_subplot(slyr_grid[slyr])]
        ax = axs[-1]

        pts += [ax.imshow(data[sec*6 + (5-slyr)],
            origin='lower',
            aspect='auto',
            interpolation='nearest',
            extent=[-0.5,111.5,-0.5,5.5])]
        if slyr == 0:
            ax.set_title('Sector '+str(sec+1))
        ax.set_ylabel(str(6-slyr))
        ax.xaxis.set_major_locator(pyplot.NullLocator())
        ax.yaxis.set_major_locator(pyplot.NullLocator())


def update(i):
    data = rand.uniform(0,100,(36,6,112))
    for sec in range(6):
        for slyr in range(6):
            i = sec*6 + slyr
            pt = pts[i]
            pt.set_data(data[i])


ani = animation.FuncAnimation(fig, update, np.arange(1, 200),interval=1)
pyplot.show()
