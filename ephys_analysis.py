__author__ = "Chad Estep (chadestep@gmail.com)"

import numpy as np
import scipy as sp
from scipy import signal
from neo import io
import pandas as pd
# import matplotlib.pyplot as plt

def read_abf(filename, groupby=False):
    """
    Imports ABF file using neo io AxonIO, breaks it down by blocks 
    which are then processed into  a multidimensional pandas dataframe 
    where each block corresponds to a sweep and columns represent time
    and each recorded channel. Channel names can be changed later if 
    necessary.
    
    More documentation necessary.

    TODO: remove final 'names' attribute from .concat?
    """
    
    r = io.AxonIO(filename = filename)
    bl = r.read_block(lazy=False, cascade=True)
    num_channels = len(bl.segments[0].analogsignals)
    df_list = []
    channels = []
    signals = []
    sweep_list = []

    for seg_num, seg in enumerate(bl.segments):
        for i in range(num_channels):
            channels.append('channel_' + str(i))
            signals.append(bl.segments[seg_num].analogsignals[i])
        data_dict = dict(zip(channels, signals))
        time = seg.analogsignals[0].times - seg.analogsignals[0].times[0]
        data_dict['time'] = time
        df = pd.DataFrame(data_dict)
        df_list.append(df)
        sweep_list.append('sweep' + str(seg_num + 1).zfill(3))
        
    if groupby:
        return pd.concat(df_list, keys=sweep_list, 
            names=['sweep']).groupby(level='sweep')
    else: 
        return pd.concat(df_list, keys=sweep_list, 
            names=['sweep'])


def rolling_window(df, window, step):
    """
    ORIGINALLY TITLED: 'create_epoch', but thought this was better
    BETA: lots of functionality to add and code to clean.

    This function takes an input DataFrame and groups it by its level=0
    index before passing it to the rest of the function to create a new
    Multiindex DataFrame with the original level=0 being the same, and
    an added level=1 being what this function creates.

    To keep things as 'simple' as possible for the other functions, the
    number of epochs has been limited to 999. If you really need more
    than that number, then just go ahead and change the source code.

    NOTE: based on your specified window and step size, your 
    new array may be truncated. 

    Inputs
    df     : input pandas dataframe
    window : epoch size based on array index
    step   : start-to-start number of rows between captured windows 
             (may overlap with other windows)
    """

    window = int(window)
    step = int(step)
    df_list = []
    sweep_list = []
    sweep_names = []
    grouped = df.groupby(level=0)

    for sweep, data in grouped:
        rows = len(grouped.get_group(sweep))
        epoch_arrays = []
        epoch_names = []
        sweep_names.append(sweep)
        num_epochs = int(1 + (rows - window) / step)
        for i in range(num_epochs):
            epoch_names.append('epoch' + str(i + 1).zfill(3))
            epoch_arrays.append(grouped.get_group(sweep)[(0 + step * i):(window + step * i)])
        data_dict = dict(zip(epoch_names, epoch_arrays)) # do i need
        # this?
        df = pd.concat(epoch_arrays, keys=epoch_names).swaplevel(0,1)
        df_list.append(df)

    return pd.concat(df_list)

def simpleaxis(ax):
    """
    (note: stolen from somewhere else, but forgot where)

    Removes the top and right axis lines and tick marks
    on standard pyplot figures. Does not work with 
    GridSpec objects (need to figure that out.)

    Input
    ax: matplotlib.pyplot axis

    """
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

def simpleaxes(ax):
    """
    THIS WILL BE REMOVED IN FUTURE RELEASES (PROBABLY...)

    Like 'simpleaxis,'' but for multiple subplots
    """
    for i, data in enumerate(ax):
        ax[i].spines['top'].set_visible(False)
        ax[i].spines['right'].set_visible(False)
        ax[i].get_xaxis().tick_bottom()
        ax[i].get_yaxis().tick_left()


def epoch_hist(epoch_df, channel, hist_min, hist_max, num_bins):
    """
    Creates a bunch of 1D histograms of the epochs created from
    ea.rolling_window function. (SO ASSUMES EPOCH'D DATAFRAME)
    """
    sweep_arrays = []
    epoch_arrays = []
    df_list = []
    sweeps = epoch_df.index.levels[0].values
    epochs = epoch_df.index.levels[1].values
    
    for sweep in sweeps:
        for epoch in epochs:
            data = epoch_df.ix[sweep][channel].xs(epoch)
            epoch_hist, bins = np.histogram(data, bins=num_bins, range=(hist_min,hist_max))
            arrays = [[sweep]*len(epoch_hist),[epoch]*len(epoch_hist),np.linspace(hist_min, hist_max, len(bins))]
            index = pd.MultiIndex.from_arrays(arrays, names=['sweep','epoch','bin'])
            df = (pd.DataFrame(epoch_hist, columns=[channel]))
            df.set_index(index, inplace=True)
            df_list.append(df)
    return pd.concat(df_list)





