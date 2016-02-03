#!/usr/bin/env python
__author__ = "Chad Estep (chadestep@gmail.com)"

""" Basic plotting functions for 1D subplot structures """

import matplotlib.pyplot as plt

"""
Note: Still need to test on much more complicated subplot structures.
"""

def simple_axis(ax):
    """
    Removes the top and right axis lines and tick marks for a single matplotlib.axes object.

    Parameters
    ----------
    ax:
        matplotlib.axes._subplots.AxesSubplot.
    """
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

def simple_figure(f):
    """
    Removes the top and right axis lines and tick marks for all axes in a matplolib figure.

    Parameters
    ----------
    f:
        matplotlib.figure.Figure object.
    """
    num_ax = len(f.axes)
    if num_ax == 1:
        simple_axis(f.axes[0])
    else:
        for i in range(num_ax):
            f.axes[i].spines['top'].set_visible(False)
            f.axes[i].spines['right'].set_visible(False)
            f.axes[i].get_xaxis().tick_bottom()
            f.axes[i].get_yaxis().tick_left()

def clean_axis(ax, y_units, **y_hline):
    """
    Removes all axis lines and tick marks for a single matplotlib.axes object.

    Parameters
    ----------
    ax:
        matplotlib.axes._subplots.AxesSubplot.
    y_units: string
        The units you want listed in your legend for the y_hline(s).
    y_hline: dict or None (default)
        Draws an arbitrary number of dotted horizontal lines at a user specified y-values that spans the entire length of the figure.
        ex: string = <int or float>
            baseline = -50.0
    """
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    for key, val in y_hline.items():
        ax.axhline(y=val,color='grey',linestyle='dotted',label='{0}: {1} {2}'.format(key,val,y_units))

def clean_figure(f, y_units, **y_hline):
    """
    Removes all axis lines and tick marks for all axes in a matplolib figure.

    Parameters
    ----------
    f:
        matplotlib.figure.Figure object.
    y_units: string
        The units you want listed in your legend for the y_hline(s).
    y_hline: dict or None (default)
        Draws an arbitrary number of dotted horizontal lines at a user specified y-values that spans the entire length of the figure.
        ex: string = <int or float>
            baseline = -50.0
    """
    num_ax = len(f.axes)
    if num_ax == 1:
        clean_axis(f.axes[0], y_units, **y_hline)
    else:
        for i in range(num_ax):
            f.axes[i].spines['top'].set_visible(False)
            f.axes[i].spines['right'].set_visible(False)
            f.axes[i].spines['bottom'].set_visible(False)
            f.axes[i].spines['left'].set_visible(False)
            f.axes[i].get_xaxis().set_visible(False)
            f.axes[i].get_yaxis().set_visible(False)
            for key, val in y_hline.items():
                f.axes[i].axhline(y=val,color='grey',linestyle='dotted',label='{0}: {1} {2}'.format(key,val,y_units))

def scaleandlegend(f, x_scale, x_units, y_scale, y_units):
    """
    Add x and y scale bars to the bottom right of the only/last subplot of a figure and a legend outside of the figure.

    Parameters
    ----------
    f:
        matplotlib.figure.Figure object.
    x_scale: int or float
        User specified length of the scale bar.
    x_units: string
        X-axis units used in the figure legend.
    y_scale: int or float
        User specified length of the scale bar.
    y_units: string
        Y-axis units used in the figure legend.
    """
    ax = f.axes[-1]
    x_min,x_max = ax.get_xlim()[0],ax.get_xlim()[1]
    y_min,y_max = ax.get_ylim()[0],ax.get_ylim()[1]
    x_range = abs(x_min-x_max)
    y_range = abs(y_min-y_max)
    hline_min = (x_scale/x_range)
    vline_max = (y_scale/y_range)
    ax.axhline(y=y_min,xmin=(1-hline_min),xmax=1,color='black',lw=2,label='x: {0} {1}'.format(x_scale,x_units))
    ax.axvline(x=x_max,ymin=0,ymax=vline_max,color='black',lw=2,label='y: {0} {1}'.format(y_scale,y_units))
    plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0, frameon=False)
