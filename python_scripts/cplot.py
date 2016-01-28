#!/usr/bin/env python
__author__ = "Chad Estep (chadestep@gmail.com)"

""" Basic plotting and helper functions (ChadPlot) """

import matplotlib.pyplot as plt

def simpleaxis(ax):
    """
    Removes the top and right axis lines and tick marks on standard
    pyplot figures. Does not work with GridSpec objects.

    Parameters
    ----------
    ax:
        Matplotlib.pyplot axis object
    """
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

def simpleaxes(ax):
    """
    Like 'simpleaxis,'' but for multiple subplots
    """
    for i, data in enumerate(ax):
        ax[i].spines['top'].set_visible(False)
        ax[i].spines['right'].set_visible(False)
        ax[i].get_xaxis().tick_bottom()
        ax[i].get_yaxis().tick_left()

def naked_plot(x, y, xlims, ylims, x_val_scale, y_val_scale,
    legend=True):
    """
    Make a minimalist plot that contains only the data and two scale
    bars (x and y).

    Parameters
    ----------
    x: array
        X-axis data.
    y: array
        Y-axis data.
    xlims: tuple
        X min and max values. Example: (0, 10)
    ylims: tuple
        Y min and max values. Example: (-70, 20)
    x_val_scale: int/float
        The x-value where you want to draw the y-axis scale bar. Bar
        will span the bottom 10% of the plot.
    y_val_scale: int/float
        The y-value where you want to draw the x-axis scale bar. Bar
        will span the rightmost 10% of the plot.
    legend: bool (default: True)
        Legend containing the size of each of your scale bars, each one being 10% of the total x or y-axis length (so make note of that number if you choose not to plot it).

    Return
    ------
    f:
        Pyplot figure object.
    ax:
        Pyplot axis object.
    """

    f, ax = plt.subplots(1)
    ax.plot(x,y)
    simpleaxis(ax)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    ax.axvline(x=x_val_scale, ymin=0, ymax=0.1, color='black', lw=2,
        label='y: {0}'.format((ylims[1]-ylims[0])/10))
    ax.axhline(y=y_val_scale, xmin=0.9, xmax=1.0, color='black', lw=2,
        label='x: {0}'.format((xlims[1]-xlims[0])/10))
    if legend == False:
        pass
    else:
        plt.legend(frameon=False)
    return f, ax

def raster(event_list, color='black'):
    """
    Creates a simple, single line, raster plot.

    Parameters
    ----------
    event_list: list of ints/floats
        List of the event times you want to plot.
    color: string (default='black')
        Color you want your raster plot

    Return
    ------
    f:
        Pyplot figure object.
    ax:
        Pyplot axis object.
    """

    f, ax = plt.subplots()
    for i in range(len(event_list)):
        ax.vlines(trial, 0, 0.1, color=color)
    return f, ax


def c_boxpot(things):
    print("i'm not done yet")
