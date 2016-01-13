__author__ = "Chad Estep (chadestep@gmail.com)"

import numpy as np
import scipy as sp
from scipy.signal import periodogram
from scipy.stats import gaussian_kde
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


def create_epoch(df, window, step):
    """
    This function takes an input DataFrame and groups it by its level=0
    index before passing it to the rest of the function to create a new
    Multiindex DataFrame with the original level=0 being the same, and
    an added level=1 being what this function creates.

    To keep things as 'simple' as possible for the other functions, the
    number of epochs has been limited to 999. If you really need more
    than that number, then just go ahead and change the source code.

    NOTE: based on your specified window and step size, your 
    new array may be truncated. 

    Input parameters
    df     : input pandas dataframe
    window : epoch size based on array index
    step   : start-to-start number of rows between captured windows 
             (may overlap with other windows)
    """

    window = int(window)
    step = int(step)
    sweep_list = []
    sweeps = df.index.levels[0].values
    num_rows = len(df.ix[df.index.levels[0][0]])
    num_epochs = int(1 + (num_rows - window) / step)
    arrays = [['sweep' + str(i + 1).zfill(3) for i in range(len(sweeps))],['epoch' + str(i + 1).zfill(3) for i in range(num_epochs)],np.arange(window)]
    index = pd.MultiIndex.from_product(arrays,names=['sweep','epoch',None])

    for sweep in sweeps:
        sweep_vals = df.ix[sweep].values
        epoch_data = np.array([sweep_vals[(0 + step * i):(window + step * i)] for i in range(num_epochs)])
        sweep_data = np.concatenate([epoch_data[i,:,:] for i in range(num_epochs)],axis=0) 
        sweep_list.append(sweep_data)
    concat_sweeps = np.concatenate(sweep_list,axis=0)
    epoch_df = pd.DataFrame(concat_sweeps,columns=df.columns.values)
    epoch_df.set_index(index,inplace=True)
    return epoch_df


def epoch_hist(epoch_df, channel, hist_min, hist_max, num_bins):
    """
    Creates a bunch of 1D histograms of the epochs created from
    ea.create_epoch function.

    Input parameters
    epoch_df: dataframe from 'create_epoch' function
    channel: channel column to be analyzed
    hist_min: minimum of histogram bin range
    hist_max: maximum of histogram bin range
    num_bins: number of bins you want

    Output df:
    'bins' column contains the 'leftmost' (smallest?) bin edge.
    """
    hist_arrays = []
    bin_arrays = []

    sweep_names = epoch_df.index.levels[0].values
    epoch_names = epoch_df.index.levels[1].values
    idx = np.arange(num_bins)
    arrays = [sweep_names,epoch_names,idx]
    index = pd.MultiIndex.from_product(arrays,names=['sweep','epoch',None])

    total_epochs = len(sweep_names)*len(epoch_names)
    epoch_size = epoch_df.ix['sweep001'][channel].xs('epoch001').size
    data = epoch_df[channel].values

    for i in range(total_epochs):
        hist, bins = np.histogram(data[(i*epoch_size):((i+1)*epoch_size)],bins=num_bins,range=(hist_min,hist_max))
        hist_arrays.append(hist)
        bin_arrays.append(bins[:num_bins])

    hist_concat = np.concatenate(hist_arrays,axis=0)
    bin_concat = np.concatenate(bin_arrays,axis=0)
    data = list(zip(bin_concat,hist_concat))
    df = pd.DataFrame(data,columns=['bin',channel])
    df.set_index(index, inplace=True)
    return df


def epoch_kde(epoch_df, channel, range_min, range_max, samples=1000):
    """
    Creates a bunch of 1D KDEs of the epochs created from
    ea.create_epoch function.

    Input parameters
    epoch_df: dataframe from 'create_epoch' function
    channel: channel column to be analyzed
    range_min: minimum of KDE range
    range_max: maximum of KDE range
    samples: number of KDE samples
    """
    
    kde_arrays = []
    x_arrays = []

    samples = samples
    sweep_names = epoch_df.index.levels[0].values
    epoch_names = epoch_df.index.levels[1].values
    idx = np.arange(samples)

    arrays = [sweep_names,epoch_names,idx]
    index = pd.MultiIndex.from_product(arrays,names=['sweep','epoch',None])
    total_epochs = len(sweep_names)*len(epoch_names)
    epoch_size = epoch_df.ix['sweep001'][channel].xs('epoch001').size
    x = np.linspace(range_min, range_max, samples)
    data = epoch_df[channel].values
    
    for i in range(total_epochs):
        kde = sp.stats.gaussian_kde(data[(i*epoch_size):((i+1)*epoch_size)])
        kde_data = kde(x)
        kde_arrays.append(kde_data)
        x_arrays.append(x)
    
    kde_concat = np.concatenate(kde_arrays,axis=0)
    x_concat = np.concatenate(x_arrays,axis=0)

    data = list(zip(x_concat,kde_concat))
    df = pd.DataFrame(data,columns=['x',channel])
    df.set_index(index, inplace=True)
    return df


def epoch_pgram(epoch_df, channel, fs=10e3):
    """
    Run periodogram on each epoch

    Input parameters
    epoch_df: dataframe from 'create_epoch' function
    channel: channel column to be analyzed
    fs: sampling frequency
    """
    
    df_list = []
    fs = fs
    sweeps = epoch_df.index.levels[0].values
    epochs = epoch_df.index.levels[1].values
    
    for sweep in sweeps:
        for epoch in epochs:
            data = epoch_df.ix[sweep][channel].xs(epoch)
            pgram_f, pgram_den = periodogram(data, fs)
            arrays = [[sweep]*len(pgram_f),[epoch]*len(pgram_f),np.arange(len(pgram_f))]
            index = pd.MultiIndex.from_arrays(arrays, names=['sweep','epoch',None])
            data_list = list(zip(pgram_f,pgram_den))
            df = pd.DataFrame(data_list, columns=['frequency',channel])
            df.set_index(index, inplace=True)
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