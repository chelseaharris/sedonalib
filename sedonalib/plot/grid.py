#
#
# Authors: Dan Kasen, Chelsea Harris
# Date: 2018-12-04
# 
# Purpose: Tools for plotting Sedona `grid` output files
#         

import numpy as np
import matplotlib.pyplot as plt

from sedonalib.loaders import choose_reader
import sedonalib.data.physical_constants as C


def plot_grid(grid_fn,
              which_log='', zone_num=0, quantity='opacity', plot_nu=False, xlim=(), ylim=(), ls='-' ):

    quantity_labels = {'opacity'   :'opacity (cm^2/g)',
                       'emissivity':'emissivity',
                       'Jnu'       :'radiation field Jnu (ergs/s/Hz/cm^2/str)'}

    # Load the grid
    assistant = choose_reader(grid_fn)
    assistant.open(grid_fn)
  
    # Get frequency for x-axis
    nu = np.array(assistant.pull_one(['nu']))
  
    # Get quantity to plot for y-axis
    if quantity=='Snu':
        zone = 'zonedata/{}'.format(zone_num)
        opac = np.array(assistant.pull_one(zone+'/opacity'))
        emis = np.array(assistant.pull_one(zone+'/emissivity'))
        vals = emis/opac
    else:
        y_field = 'zonedata/{}/{}'.format(zone_num,quantity)
        vals = np.array(assistant.pull_one(y_field))
  
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


