#!/usr/bin/env python
__author__ = "Chad Estep (chadestep@gmail.com)"

""" Basic plotting functions for 1D subplot structures """

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('estep_style')

def nu_boxplot(df, medians_only=False, show_outliers=True, **y_hline):
    """
    Makes a much improved boxplot.

    Parameters
    ----------
    df: pandas DataFrame
        Pandas Dataframe where each of the columns makes a separate boxplot.
        Column names will be used as x-axis labels.
    medians_only: bool (default=False)
        Default changes the entire boxplot the new color,
        but if True only changes the color of the median bar.
    showfliers: bool (default=True)
        Turns outliers on or off.
    y_hline: dict or None (default=None)
        Draws an arbitrary number of dotted horizontal lines at a user specified
        y-values that spans the entire length of the figure.
        ex: string = <int or float>
            baseline = -50.0

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
#     NEED TO MAKE SURE THIS IS CALLED PROPERLY IN THE FINISHED VERSION!
    simple_axis(ax)
    return f, ax

def scatter_col(df, alpha=0.35, jitter=0.05, markersize=8, monocolor=False, seed=0):
    """
    Creates a scatter column plot.

    Parameters
    ----------
    df: pandas DataFrame
        Pandas Dataframe where each of the columns makes a separate scatter column plot. Column names will be used as x-axis labels (eventually).
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

    TO DO:
    - add y_label param?
    - fix jitter setting to keep perfectly consistent across plots
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

    ax.set_xlim(0.5, column_num+0.5)
    ax.xaxis.set_ticks(np.arange(1, column_num+1))
    ax.xaxis.set_ticklabels(labels, rotation=45)
    simple_axis(ax)
    return f, ax
