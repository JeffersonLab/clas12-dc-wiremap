import numpy as np
from numpy import random as rand
from scipy import stats
from scipy import optimize as opt
from matplotlib import pyplot

# setup the data
npoints = 10000
sample_data = rand.normal(0,2,npoints)

# histogram the data
h,e = np.histogram(sample_data, bins=100, range=[-10,10])

# get centers of the bins of histogram
bin_centers = 0.5*(e[1:] + e[:-1])
#starting at 2 element and then shifting everything to the left by 1

# setup the function to fit to the data
def gauss(x,N,mean,sigma):
    return N * stats.norm(mean,sigma).pdf(x) #fitting 'norm' distribution

# guess initial parameters
p0 = [npoints,0,2]

# fit the function to the data
popt,pcov = opt.curve_fit(gauss,bin_centers,h,p0)

# make (x,y) points using the fitted parameters
xx = np.linspace(-10,10,300)
yyfit = gauss(xx,*popt)

# plot the data and the fitted curve
fig,ax = pyplot.subplots()
ax.errorbar(bin_centers,h,yerr=np.sqrt(h),xerr=0.5*(e[1]-e[0]),
    linestyle='none')
ax.plot(xx,yyfit)

pyplot.show()
