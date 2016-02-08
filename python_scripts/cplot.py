#!/usr/bin/env python
__author__ = "Chad Estep (chadestep@gmail.com)"

""" Plotting helper functions for publication quality figures """

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
# using my style not necessary, but highly encouraged
plt.style.use('estep_style')

def simple_axis(ax):
    """
    Removes the top and right axis lines and tick marks for a single matplotlib.axes object.

    Parameters
    ----------
    ax:
        Matplotlib axes object.
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
        Matplotlib figure object.
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
        Matplotlib axes object.
    y_units: string
        The units you want listed in your legend for the y_hline(s).
    y_hline: key-value pair or None (default)
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
        Matplotlib figure object.
    y_units: string
        The units you want listed in your legend for the y_hline(s).
    y_hline: key-value pair or None (default)
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
        Matplotlib figure object.
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

def nu_boxplot(ax, df, medians_only=False, show_outliers=True, **y_hline):
    """
    Makes a much improved boxplot.

    Parameters
    ----------
    ax:
        matplotlib axes object
    df: pandas DataFrame
        Pandas Dataframe where each column makes a separate boxplot. Column names will be used as x-axis labels.
    medians_only: bool (default=False)
        Default changes the entire boxplot the new color,
        but if True only changes the color of the median bar.
    showfliers: bool (default=True)
        Turns outliers on or off.
    y_hline: key-value pair or None (default=None)
        Draws an arbitrary number of dotted horizontal lines at user specified y-value that spans the entire length of the figure.
        ex: string = <int or float>
            baseline = -50.0

    Returns
    -------
    bp: dict of matplolib objects
        Contains all the necessary boxplot parameters, and when properly assigned to a matplotlib axes object will render your boxplot.

    TO DO:
        - Add y_label param??
    """
    # set up basic plotting values and parameters
    data = df.dropna().values
    if df.ndim == 1:
        column_num = 1
        labels = [df.name]
    else:
        column_num = df.shape[1]
        labels = df.columns.values
    # make the basic figure with better default properties.
    bp = ax.boxplot(data,
                    showfliers=show_outliers,
                    boxprops=dict(color='000000',linestyle='-',linewidth=2),
                    capprops=dict(color='000000',linestyle='-',linewidth=2),
                    flierprops=dict(linestyle='none',marker='.',markeredgecolor='000000',
                                    markerfacecolor='000000',markersize=5),
                    labels=labels,
                    medianprops=dict(color='000000',linestyle='-',linewidth=4),
                    widths=0.5,
                    whis=[10,90],
                    whiskerprops=dict(color='000000',linestyle='-',linewidth=2))
    # reset the colors based on style sheet currently in use
    colors = [i['color'] for i in mpl.rcParams['axes.prop_cycle']]
    if medians_only:
        for i in range(column_num):
            color = colors[i]
            mpl.artist.setp(bp['medians'][i], color=color)
    else:
        for i in range(column_num):
            color = colors[i]
            mpl.artist.setp(bp['boxes'][i], color=color)
            mpl.artist.setp(bp['caps'][i*2], color=color)
            mpl.artist.setp(bp['caps'][i*2+1], color=color)
            mpl.artist.setp(bp['medians'][i], color=color)
            mpl.artist.setp(bp['whiskers'][i*2], color=color)
            mpl.artist.setp(bp['whiskers'][i*2+1], color=color)
            if show_outliers:
                mpl.artist.setp(bp['fliers'][i], markerfacecolor=color, markeredgecolor=color)
    # add in an optional line
    for key, val in y_hline.items():
        ax.axhline(y=val,color='grey',linestyle='dotted')
    # make final changes to plot to clean it up and make it pretty
    ax.xaxis.set_ticklabels(labels, rotation=45)
    simple_axis(ax)
    return bp

def scatter_col(ax, df, alpha=0.35, jitter=0.05, markersize=8, monocolor=False, seed=0):
    """
    Creates a scatter column plot.

    Parameters
    ----------
    ax:
        Matplotlib axes object
    df: pandas DataFrame
        Pandas Dataframe where each column makes a separate scatter column plot. Column names will be used as x-axis labels.
    alpha: float (0.0 through 1.0)
        Sets marker opacity. 0.0 = transparent through 1.0 = opaque.
    jitter: float (0.0 through 1.0, default=0.35)
        Sets the amount of jitter in the column data. The default value keeps the scatter to roughly between the whiskers. 0.0 = no jitter through 1.0 = jitter the width of the plot. Can technically go past 1.0, but at that point you lose data from the figure, so do not do that.
    markersize: float
        Sets the size of the scatter plot marker.
    monocolor: any matplotlib color (default=False)
        Set all scatter plot objects to the specificed color.
    seed:
        Sets the numpy.random.seed value that controls the jitter of the resulting plots. Same data + same seed = same figure.

    Returns
    -------
    sc: list of matplolib objects
        Contains all the necessary scatterplot parameters, and when properly assigned to a matplotlib axes object will render your scatterplot.

    TO DO:
    - add y_label param?
    - add jitter scaling to keep perfectly consistent across plots
    """
    np.random.seed(seed)
    data = df.values
    if df.ndim == 1:
        column_num = 1
        labels = [df.name]
    else:
        column_num = df.shape[1]
        labels = df.columns.values

    for i in range(column_num):
        if column_num == 1:
            y = data
        else:
            y = data[:,i]
        x = np.random.normal(i+1, jitter, size=len(y))
        sc = ax.plot(x,y,
                     alpha=alpha,
                     linestyle='None',
                     label=labels[i],
                     marker='.',
                     markersize=markersize)
        if monocolor:
            mpl.artist.setp(sc[0], markeredgecolor=monocolor,markerfacecolor=monocolor)
    ax.set_xlim(0.5, column_num+0.5)
    ax.xaxis.set_ticks(np.arange(1, column_num+1))
    ax.xaxis.set_ticklabels(labels, rotation=45)
    simple_axis(ax)
    return sc

def raster(ax, df, color='00000', **x_vline):
    """
    Creates a raster plot that reads top-down and left-right.

    Parameters
    ----------
    ax:
        Matplotlib ax object
    df: pandas DataFrame
        Pandas Dataframe where each column makes a separate raster plot. THE PLOT WILL READ IN THE EXACT SAME MANNER AS 'df.T' LOOKS.
    color: any valid matplotlib color
    x_vline: key-value pair or None (default=None)
        Draws an arbitrary number of dotted horizontal lines at user specified y-value that spans the entire length of the figure.

    Returns
    -------
    ras: matplotlib.collections.LineCollection
        Contains all the necessary raster parameters, and when properly assigned to a matplotlib axes object will render your raster plot.

    Heavily adapted from:
    [1] https://scimusing.wordpress.com/2013/05/06/making-raster-plots-in-python-with-matplotlib/

    TO DO:
    - y label?
    - bottom up option?
    - line width?
    """
    if df.ndim == 1:
        ras = ax.vlines(df.T.values,0.5,1.5,color=color)
    else:
        data = df.T.values
        for i, sweep in enumerate(data):
            ras = ax.vlines(sweep,i+0.5,i+1.5,color=color)

    # add in an optional line
    for key, val in x_vline.items():
        ax.axvline(x=val,color='grey',linestyle='dotted')

    # set up the axis and labels so that they properly label sweeps
    ax.set_ylim(0.5,len(data)+0.5)
    ax.set_yticks(np.arange(1,data.shape[0]+1,1))
    ax.invert_yaxis()
    simple_axis(ax)
    return ras

def standalone_nu_boxplot(df, medians_only=False, show_outliers=True, **y_hline):
    """
    Makes a much improved boxplot.

    Parameters
    ----------
    df: pandas DataFrame
        Pandas Dataframe where each of the columns makes a separate boxplot.
        Column names will be used as boxplot labels.
    medians_only: bool (default=False)
        Default changes the entire boxplot the new color,
        but if True only changes the color of the median bar.
    showfliers: bool (default=True)
        Turns outliers on or off.
    y_hline: key-value pair or None (default=None)
        Draws an arbitrary number of dotted horizontal lines at a user specified
        y-values that spans the entire length of the figure.
        ex: string = <int or float>
            baseline = -50.0

    Returns
    -------
    f:
        Matplotlib figure object.
    ax:
        Matplotlib axes object.

    TO DO:
        - Add ylabel?
    """
    # set up basic plotting values and parameters
    data = df.dropna().values
    if df.ndim == 1:
        column_num = 1
        labels = [df.name]
    else:
        column_num = df.shape[1]
        labels = df.columns.values
    # make the basic figure with better default properties.
    f, ax = plt.subplots(1, figsize=(column_num,5))
    bp = plt.boxplot(data,
                     showfliers=show_outliers,
                     boxprops=dict(color='000000',linestyle='-',linewidth=2),
                     capprops=dict(color='000000',linestyle='-',linewidth=2),
                     flierprops=dict(linestyle='none',marker='.',markeredgecolor='000000',
                                     markerfacecolor='000000',markersize=5),
                     labels=labels,
                     medianprops=dict(color='000000',linestyle='-',linewidth=4),
                     widths=0.5,
                     whis=[10,90],
                     whiskerprops=dict(color='000000',linestyle='-',linewidth=2))
    # reset the colors based on user input
    colors = [i['color'] for i in plt.rcParams['axes.prop_cycle']]
    if medians_only:
        for i in range(column_num):
            color = colors[i]
            plt.setp(bp['medians'][i], color=color)
    else:
        for i in range(column_num):
            color = colors[i]
            plt.setp(bp['boxes'][i], color=color)
            plt.setp(bp['caps'][i*2], color=color)
            plt.setp(bp['caps'][i*2+1], color=color)
            plt.setp(bp['medians'][i], color=color)
            plt.setp(bp['whiskers'][i*2], color=color)
            plt.setp(bp['whiskers'][i*2+1], color=color)
            if show_outliers:
                plt.setp(bp['fliers'][i], markerfacecolor=color, markeredgecolor=color)
    # add in an optional line
    for key, val in y_hline.items():
        plt.axhline(y=val,color='grey',linestyle='dotted')
    # make final changes to plot to clean it up and make it pretty
    plt.xticks(rotation=45)
    simple_axis(ax)
    return f, ax

def standalone_scatter_col(df, alpha=0.35, jitter=0.05, markersize=8, monocolor=False, seed=0):
    """
    Creates a scatter column figure.

    Parameters
    ----------
    ax:
        Matplotlib axes object
    df: pandas DataFrame
        Pandas Dataframe where each column makes a separate scatter column plot. Column names will be used as x-axis labels.
    alpha: float (0.0 through 1.0)
        Sets marker opacity. 0.0 = transparent through 1.0 = opaque.
    jitter: float (0.0 through 1.0, default=0.35)
        Sets the amount of jitter in the column data. The default value keeps the scatter to roughly between the whiskers. 0.0 = no jitter through 1.0 = jitter the width of the plot. Can technically go past 1.0, but at that point you lose data from the figure, so do not do that.
    markersize: float
        Sets the size of the scatter plot marker.
    monocolor: any matplotlib color (default=False)
        Set all scatter plot objects to the specificed color.
    seed:
        Sets the numpy.random.seed value that controls the jitter of the resulting plots. Same data + same seed = same figure.

    Returns
    -------
    f:
        Matplotlib figure object.
    ax:
        Matplotlib axes object.

    TO DO:
    - add y_label param?
    """
    # set up basic plotting values and parameters
    np.random.seed(seed)
    data = df.values
    if df.ndim == 1:
        column_num = 1
        labels = [df.name]
    else:
        column_num = df.shape[1]
        labels = df.columns.values
    # crete an appropriately sized figure for the dataset
    f, ax = plt.subplots(1, figsize=(column_num,5))
    for i in range(column_num):
        if column_num == 1:
            y = data
        else:
            y = data[:,i]
        x = np.random.normal(i+1, jitter, size=len(y))
        sp = plt.plot(x, y,
                      alpha=alpha,
                      linestyle='None',
                      label=labels[i],
                      marker='.',
                      markersize=markersize)
        if monocolor:
            plt.setp(sp[0], markeredgecolor=monocolor,markerfacecolor=monocolor)
    # make final changes to plot to clean it up and make it pretty
    ax.set_xlim(0.5, column_num+0.5)
    ax.xaxis.set_ticks(np.arange(1, column_num+1))
    ax.xaxis.set_ticklabels(labels, rotation=45)
    simple_axis(ax)
    return f, ax
