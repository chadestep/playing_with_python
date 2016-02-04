#!/usr/bin/env python
__author__ = "Chad Estep (chadestep@gmail.com)"

""" Basic plotting functions for 1D subplot structures """

import matplotlib.pyplot as plt

def nu_boxplot(df,medians_only=False):
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
    """
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
               boxprops=dict(color='000000',linestyle='-',linewidth=2),
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
            plt.setp(bp['fliers'][i], markerfacecolor=color, markeredgecolor=color)
            plt.setp(bp['medians'][i], color=color)
            plt.setp(bp['whiskers'][i*2], color=color)
            plt.setp(bp['whiskers'][i*2+1], color=color)

    plt.xticks(rotation=45)
#     NEED TO MAKE SURE THIS IS CALLED PROPERLY IN THE FINISHED VERSION!
    simple_axis(ax)
    return f, ax
