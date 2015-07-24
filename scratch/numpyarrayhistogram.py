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

a = rand.normal(100,10,(6,6,6,112))
b = a + rand.normal(0,1,a.shape)
#ravel into 1D for histogram
H, e = np.histogram((a-b).ravel(), bins = 100, range=(-10,10))

bin_centers = 0.5*(e[1:] + e[:-1])
#starting at 2 element and then shifting everything to the left by 1

# setup the function to fit to the data
def gauss(x,N,mean,sigma):
    return N * stats.norm(mean,sigma).pdf(x) #fitting 'norm' distribution

# guess initial parameters
p0 = [H.sum(),0,1]

# fit the function to the data
popt,pcov = opt.curve_fit(gauss,bin_centers,H,p0)

# make (x,y) points using the fitted parameters
xx = np.linspace(-10,10,300)
yyfit = gauss(xx,*popt)

# plot the data and the fitted curve
fig,ax = pyplot.subplots()
ax.errorbar(bin_centers,H,yerr=np.sqrt(H),xerr=0.5*(e[1]-e[0]),
    linestyle='none')
ax.plot(xx,yyfit)

pyplot.show()



'''
xx = 0.5*(edges[:-1] + edges[1:])
fig,ax = pyplot.subplots()
ax.errorbar(xx,H,xerr=0.5*(xx[1]-xx[0]),yerr=np.sqrt(H), linestyle='none')

pyplot.show()

'''
