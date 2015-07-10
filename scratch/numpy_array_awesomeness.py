import numpy as np
from matplotlib import pyplot

def transform(a):
    a.shape = (6,6*6,112)
    a[3:,:,...] = a[3:,::-1,...]
    a.shape = (2,3,6,6,112)
    a = np.rollaxis(a,2,1)
    a = np.rollaxis(a,3,2)
    a = a.reshape(2*6*6,3*112)
    a = np.roll(a,6*6,axis=0)
    return a

a = np.arange(6*6*6*112,dtype=np.int)
a.shape = (6,6,6,112)

a[4,2,2:6,10:50] = 30000

fig = pyplot.figure()
ax = fig.add_subplot(1,1,1)
ax.imshow(transform(a), extent=[1,112*3,-6*6+1,6*6],
    aspect='auto', origin='lower', interpolation='nearest')
ax.grid(True)

_=ax.xaxis.set_ticks([1,112,112*2,112*3])
_=ax.xaxis.set_ticklabels([1,112,112,112])

yticks = list(np.linspace(-35,0,6+1,dtype=int)) + list(np.linspace(1,36,6+1,dtype=int))
ylabels = list(np.linspace(-36,0,6+1,dtype=int)) + list(np.linspace(1,36,6+1,dtype=int))
ylabels = [abs(x) for x in ylabels]
ylabels[6] = 1

del yticks[6]
del ylabels[6]
del yticks[6]
del ylabels[6]

_=ax.yaxis.set_ticks(yticks)
_=ax.yaxis.set_ticklabels(ylabels)

for sec in range(6):
    _ = ax.text(0.34*(sec%3) + 0.1, 1.02 if sec<3 else -0.06,
                'Sector {}'.format(sec+1),
                transform=ax.transAxes)

pyplot.show()
