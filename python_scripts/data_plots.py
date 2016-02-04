#!/usr/bin/env python
__author__ = "Chad Estep (chadestep@gmail.com)"

""" Basic plotting functions for 1D subplot structures """

import matplotlib.pyplot as plt

def boxplot_all(df):
    """
    Parameters
    ----------
    """
    data = df.dropna().values
    if df.ndim == 1:
        column_num = 1
        labels = [df.name]
    else:
        column_num = df.shape[1]
        labels = df.columns.values
    f, ax = plt.subplots(1, figsize=(column_num,5))
    ax.boxplot(data,
               labels=labels,
               widths=0.5,
               whis=[10,90],
               whiskerprops=dict(linestyle='-',linewidth=2,color='black'),
               boxprops=dict(linestyle='-',linewidth=2,color='black'),
               medianprops=dict(linestyle='-',linewidth=6,color='red'),
               flierprops=dict(marker='.',markerfacecolor='black',
                               markeredgecolor='black',markersize=5,linestyle='none'))
    plt.xticks(rotation=45)
#     NEED TO MAKE SURE THIS IS CALLED PROPERLY IN THE FINISHED VERSION!
    simple_axis(ax)
    return f, ax

def boxplot_series(df):
    """
    """
    if df.ndim == 1:
        boxplot_all(df)
    else:
        column_num = df.shape[1]
        data = df.dropna().values
        labels = df.columns.values
        colors = [i['color'] for i in plt.rcParams['axes.prop_cycle']]
        f, ax = plt.subplots(1, column_num, figsize=(column_num,5), sharey=True)
        for i in range(column_num):
            color = colors[i]
            ax[i].boxplot(data[:,i],
                          widths=0.5,
                          whis=[10,90],
                          capprops=dict(color=color),
                          whiskerprops=dict(linestyle='-',linewidth=2,color=color),
                          boxprops=dict(linestyle='-',linewidth=2,color=color),
                          medianprops=dict(linestyle='-',linewidth=6,color=color),
                          flierprops=dict(marker='.',markerfacecolor=color,markeredgecolor=color,
                                          markersize=5,linestyle='none'))
            ax[i].set_xticklabels(labels[i], rotation=45)
            if i < 1:
                simple_axis(ax[i])
            else:
                simple_axis(ax[i])
                ax[i].spines['left'].set_visible(False)
                ax[i].get_yaxis().set_visible(False)
        return f, ax
