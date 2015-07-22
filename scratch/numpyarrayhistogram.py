import numpy as np
#import scipy as sp

from numpy import random as rand
#from scipy import special
#from scipy import stats
#from scipy import integrate
#from scipy import optimize as opt
#from scipy import interpolate as interp

from matplotlib import pyplot
from matplotlib import cm
from matplotlib.colors import LogNorm

a = rand.normal(100,10,(50,50))
b = a + rand.normal(0,1,a.shape)
b[20,30] = 0

H, edges = np.histogram((a-b).ravel(), bins = 100, range=(-10,10))
xx = 0.5*(edges[:-1] + edges[1:])
fig,ax = pyplot.subplots()
ax.errorbar(xx,H,xerr=0.5*(xx[1]-xx[0]),yerr=np.sqrt(H), linestyle='none')

'''
fig,ax = pyplot.subplots(1,5, figsize=(12,3))
fig.subplots_adjust(wspace=.5)
pt = []
pt.append(ax[0].imshow(a,   aspect='auto', interpolation='nearest'))
pt.append(ax[1].imshow(b,   aspect='auto', interpolation='nearest'))
pt.append(ax[2].imshow(a-b, aspect='auto', interpolation='nearest'))
pt.append(ax[3].imshow(a/b, aspect='auto', interpolation='nearest'))
pt.append(ax[4].imshow((a/b)[17:23,27:33], aspect='auto', interpolation='nearest'))
for _a,p in zip(ax,pt):
    fig.colorbar(p,ax=_a)
    
n, bins, patches = pylab.hist((a-b), 10, normed=1, histtype='bar', stacked=True)
'''
pyplot.show()

