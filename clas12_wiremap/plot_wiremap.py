import numpy as np
from matplotlib import pyplot, cm, colors, colorbar

def transform(a):
    a = a.copy().reshape(6,6*6,112)
    a[3:,:,...] = a[3:,::-1,...]
    a.shape = (2,3,6,6,112)
    a = np.rollaxis(a,2,1)
    a = np.rollaxis(a,3,2)
    a = a.reshape(2*6*6,3*112)
    a = np.roll(a,6*6,axis=0)
    return a

def plot_wiremap(ax,data,**kwargs):

    cbstyle = kwargs.pop('cbstyle','discrete')

    im = ax.imshow(transform(data), extent=[1,112*3,-6*6+1,6*6],
        aspect='auto', origin='lower', interpolation='nearest')
    ax.grid(True)

    _=ax.xaxis.set_ticks([1,112,112*2,112*3])
    _=ax.xaxis.set_ticklabels([1,112,112,112])

    yticks = list(np.linspace(-35,0,6+1,dtype=int)) \
        + list(np.linspace(1,36,6+1,dtype=int))
    ylabels = list(np.linspace(-36,0,6+1,dtype=int)) \
        + list(np.linspace(1,36,6+1,dtype=int))
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

    if cbstyle == 'discrete':
        cb = discrete_colorbar(ax, im, data.max(),**kwargs)
    else:
        cb = ax.figure.colorbar(im, ax=ax)

    return im, cb

def discrete_colorbar(ax, im, zmax, cmap=cm.jet):
    zmax = int(zmax)
    # extract all colors from the map
    cmaplist = [cmap(i) for i in range(cmap.N)]

    # force the first color entry to be grey
    cmaplist[0] = (.5,.5,.5,1.0)

    # create the new map
    cmap = cmap.from_list('Discrete Colormap', cmaplist, cmap.N)

    # define the bins and normalize
    bounds = np.linspace(-0.5,zmax+0.5,zmax + 2)
    ticks = np.linspace(0,zmax,zmax+1,dtype=int)
    norm = colors.BoundaryNorm(bounds, cmap.N)

    if len(ticks) > 20:
        ticks = ticks[::len(ticks)//10]

    im.set_cmap(cmap)
    im.set_norm(norm)

    # create a second axes for the colorbar
    kw = dict(
        cmap=cmap,
        norm=norm,
        spacing='proportional',
        ticks=ticks,
        boundaries=bounds,
        format='%1i')

    from mpl_toolkits.axes_grid1 import make_axes_locatable
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size=0.15, pad=0.1)
    cb = colorbar.ColorbarBase(cax,**kw)

    cax.set_ylabel('ID Number', size=12)

    return cb,cax
