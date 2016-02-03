#!/usr/bin/env python
__author__ = "Chad Estep (chadestep@gmail.com)"

""" Basic plotting functions for 1D subplot structures """

import matplotlib.pyplot as plt

def boxplot_all(data_array):
    """
    Basic functionality is there, but need to make sure it doesn't break,
    and need to add  optional arguments (like labels, maybe colors)

    Parameters
    ----------
    data_array: 2D list of lists

    """
    whis=[10,90]
    boxprops = dict(linestyle='-',linewidth=2,color='black')
    medianprops = dict(linestyle='-',linewidth=6,color='red')
    flierprops = dict(marker='.',markerfacecolor='black',markeredgecolor='black',markersize=5,linestyle='none')
    whiskerprops = dict(linestyle='-',linewidth=2,color='black')

    f, ax = plt.subplots(1, figsize=(len(data_array),5))
    ax.boxplot(data_array,
               widths=0.5,
               whis=whis,
               whiskerprops=whiskerprops,
               boxprops=boxprops,
               medianprops=medianprops,
               flierprops=flierprops)
    plt.xticks(rotation=45)
#     NEED TO MAKE SURE THIS IS CALLED PROPERLY!
    simple_axis(ax)
    return f, ax


def boxplot_series(data_array):
    """cycles through colors, and makes plots independent but they do share a y-axis

    """

    estep_color_list = [i['color'] for i in plt.rcParams['axes.prop_cycle']]
#     estep_color_list

    whis=[10,90]
    boxprops = dict(linestyle='-',linewidth=2,color='black')
    medianprops = dict(linestyle='-',linewidth=6,color=estep_color_list[i])
    flierprops = dict(marker='.',markerfacecolor='black',markeredgecolor='black',markersize=5,linestyle='none')
    whiskerprops = dict(linestyle='-',linewidth=2,color='black')

    f, ax = plt.subplots(1,len(data_array), figsize=(len(data_array),5), sharey=True)
    for i in range(len(data_array)):
        color = estep_color_list[i]
        ax[i].boxplot(data_array[i],
#                       labels=['data'],
                      widths=0.5,
                      whis=whis,
                      capprops=dict(color=color),
                      whiskerprops=dict(linestyle='-',linewidth=2,color=color),
                      boxprops=dict(linestyle='-',linewidth=2,color=color),
                      medianprops=dict(linestyle='-',linewidth=6,color=color),
                      flierprops=dict(marker='.',markerfacecolor=color,markeredgecolor=color,markersize=5,linestyle='none'))
        if i < 1:
            simple_axis(ax[i])
        else:
            simple_axis(ax[i])
    #         a few more to clean up the boarders of the other plots
            ax[i].spines['left'].set_visible(False)
            ax[i].get_yaxis().set_visible(False)
    return f, ax
