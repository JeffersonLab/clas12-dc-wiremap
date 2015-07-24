import numpy as np
import scipy as sp

from numpy import random as rand
from scipy import special
from scipy import stats
from scipy import integrate
from scipy import optimize as opt
from scipy import interpolate as interp

from matplotlib import pyplot
from matplotlib import cm
from matplotlib.colors import LogNorm

from clas12_wiremap import plot_wiremap

a = rand.normal(100,10,(6,6,6,112))
b = a + rand.normal(0,1,a.shape)
#ravel into 1D for histogram
H, e = np.histogram((a-b).ravel(), bins = 100, range=(-10,10))

bin_centers = 0.5*(e[1:] + e[:-1])
#starting at 2 element and then shifting everything to the left by 1

# setup the function to fit to the data
def gauss(x,N,mean,sigma):
    return N * stats.norm(mean,sigma).pdf(x)  #fitting 'norm' distribution

def logistic(x,N,mean,sigma):
    return N * stats.logistic(mean,sigma).pdf(x)

def cauchy(x,N,mean,sigma):
    return N * stats.cauchy(mean,sigma).pdf(x)

# guess initial parameters
p0 = [H.sum(),0,1]

# fit the function to the data
popt1,pcov1 = opt.curve_fit(gauss,bin_centers,H,p0)
popt2,pcov2 = opt.curve_fit(logistic,bin_centers,H,p0)
popt3,pcov3 = opt.curve_fit(cauchy,bin_centers,H,p0)

# make (x,y) points using the fitted parameters
xx = np.linspace(-10,10,300)
yyfit1 = gauss(xx,*popt1)
yyfit2 = logistic(xx,*popt2)
yyfit3 = cauchy(xx,*popt3)

# plot the data and the fitted curve
fig,ax = pyplot.subplots()
ax.errorbar(bin_centers,H,yerr=np.sqrt(H),xerr=0.5*(e[1]-e[0]),
    linestyle='none')
ax.plot(xx,yyfit1)
ax.plot(xx,yyfit2)
ax.plot(xx,yyfit3)

#plotting actual wiremaps
fig,ax = pyplot.subplots()
pt, cb = plot_wiremap(ax,a,cbstyle=None)
fig,ax = pyplot.subplots()
pt, cb = plot_wiremap(ax,b,cbstyle=None)
fig,ax = pyplot.subplots()
pt, cb = plot_wiremap(ax,(a/b),cbstyle=None)

pyplot.show()


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


