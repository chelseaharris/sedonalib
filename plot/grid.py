#
#
# Authors: Dan Kasen, Chelsea Harris
# Date: 2018-12-04
# 
# Purpose: Tools for plotting Sedona `grid` output files
#         

import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('..')
import loaders.file_reader as fread
import physical_constants as C


def plot_grid(grid_fn,
              which_log='', zone_num=0, quantity='opacity', plot_nu=False, xlim=(), ylim=(), ls='-' ):

    quantity_labels = {'opacity'   :'opacity (cm^2/g)',
                       'emissivity':'emissivity',
                       'Jnu'       :'radiation field Jnu (ergs/s/Hz/cm^2/str)'}

    y_field = 'zonedata/{}/{}'.format(zone_num,quantity)

    assistant = fread.choose_reader(grid_fn)


    # Load the grid
    with h5py.File(grid_fn,'r') as data:
        # path in the HDF5 file
        zone = 'zonedata/{}'.format(zone_num)
      
        # Get frequency for x-axis
        nu = np.array(data['nu'])
      
        # Get quantity to plot for y-axis
        if quantity=='Snu':
            opac = np.array(data[zone+'/opacity'])
            emis = np.array(data[zone+'/emissivity'])
            vals = emis/opac
        else:
            vals = np.array(data[zone + '/' + type])
      
        # Plot
        if plot_nu:
            plt.plot(nu, vals, ls=ls)
        else:
            # Convert from frequency to wavelength if desired
            lm = C.LIGHT_SPEED*nu/C.ANG_PER_CM
            plt.plot(lm, vals, ls=ls)
        
        if quantity in quantity_labels.keys():
            ylabel = quantity_labels[quantity]
        else:
            ylabel = quantity
      
        if 'x' in which_log:
            plt.xscale('log')
        if 'y' in which_log:
            plt.yscale('log')
      
        if len(xlim)==2:
            plt.xlim(xlim)
        
        if len(ylim)==2:
            plt.ylim(ylim)
      
        plt.ion()
        plt.show()


