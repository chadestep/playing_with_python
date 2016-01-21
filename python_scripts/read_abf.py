#!/usr/bin/env python
__author__ = "Dan Galtieri and Chad Estep (chadestep@gmail.com)"

from neo import io
import pandas as pd

def read_abf(filename):
    """
    Imports ABF file using neo io AxonIO, breaks it down by blocks
    which are then processed into a multidimensional pandas dataframe
    where each block corresponds to a sweep and columns represent time
    and each recorded channel.

    Parameters
    ----------
    filename: str
        filename WITH '.abf' extension

    Returns
    ------_
    df: DataFrame
        Pandas DataFrame broken down by sweep

    References
    ----------
    [1] https://neo.readthedocs.org/en/latest/index.html
    """
    # use AxonIO to pull abf into python
    r = io.AxonIO(filename = filename)
    # stack and store all the blocks (check the Neo docs)
    bl = r.read_block(lazy=False, cascade=True)
    # figure out how many channels your abf has
    num_channels = len(bl.segments[0].analogsignals)
    # call the first channel 'primary' regardless
    channels = ['primary']
    # make empty lists for later appending
    signals = []
    df_list = []
    sweep_list = []

    # begin a loop for each of the segments (sweeps) in the file blocks
    for seg_num, seg in enumerate(bl.segments):
        # read in and store each of the recorded channels
        for i in range(num_channels):
            signals.append(bl.segments[seg_num].analogsignals[i])
            if i >= 1:
                channels.append('channel_' + str(i))
        # create a dictionary of the resulting data. associating channel names with channel data
        data_dict = dict(zip(channels, signals))
        time = seg.analogsignals[0].times - seg.analogsignals[0].times[0]
        # add the 'time' signal into the data dictionary
        data_dict['time'] = time
        # create a dataframe from the resulting dictionary
        df = pd.DataFrame(data_dict)
        # append the dataframe to the df_list, to be concatenated later
        df_list.append(df)
        # make a new sweep name and append it to the list
        sweep_list.append('sweep' + str(seg_num + 1).zfill(3))
        # pretty sure this doesn't need to be indented...
        df = pd.concat(df_list, keys=sweep_list, names=['sweep'])
    return df
