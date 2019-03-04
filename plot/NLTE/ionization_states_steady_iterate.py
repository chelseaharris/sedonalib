### Author: Nathaniel Roth
### Originally developed with python 2.7.13 and numpy 1.15.4

### For displaying ionization state information as output in plt files for a calculation that has run in steady_iterate mode, with atomic level data printed in the plt files

### You specify "blocks" of iterations you'd like to average together, then plot the ionization state as a function of position (zone index) for each of those blocks

### Assumes every plt file has same number of zones, and assumes that every zone of every plt file tracks the same list of elements (although that list may vary from run to run)

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import h5py
import numpy as np
import matplotlib
#matplotlib.use("agg")
import matplotlib.pyplot as plt
from matplotlib import cm
import sys

#####  PRIMARY INPUT   ######

#specify the blocks of iterations you wish to average together

iterations = [
    np.arange(90,100),
    np.arange(190,200),
    np.arange(290,300),
    np.arange(390,400),
    np.arange(490,500),
    
]

##### END PRIMARY INPUT ######

filename_prefix = 'plt_'
n_blocks = len(iterations)

# add padding zeros, assemble file list
print "Validating files"
filenames = []
for block_index in range(n_blocks):
    
    blocklist = []
    for i in range(len(iterations[block_index])):

        if (iterations[block_index][i] >= 100000 or iterations[block_index][i] < 0):
            print "invalid iterations specified"
            sys.exit()
        try:
            if (iterations[block_index][i] < 10):
                name = filename_prefix + '0000' + str(iterations[block_index][i]) + '.h5'
            if (iterations[block_index][i] >= 10 and iterations[block_index][i] < 100):
                name = filename_prefix + '000' + str(iterations[block_index][i]) + '.h5'
            if (iterations[block_index][i] >= 100 and iterations[block_index][i] < 1000):
                name = filename_prefix + '00' + str(iterations[block_index][i]) + '.h5'
            if (iterations[block_index][i] >= 1000 and iterations[block_index][i] < 10000):
                name = filename_prefix + '0' + str(iterations[block_index][i]) + '.h5'
            if (iterations[block_index][i] >= 10000 and iterations[block_index][i] < 100000):
                name = filename_prefix + str(iterations[block_index][i]) + '.h5'
            blocklist.append(name)

            # test whether you can open the file
            fin = h5py.File(name,'r')
        except:
            print "Can't find required files"
            sys.exit()
            
    filenames.append(blocklist)

# Get number of zones 
fin = h5py.File(filenames[0][0],'r')
n_zones = len(np.array(fin['r']))

# Get list of elements and their ionization states
elements = []
# Get list of elements and ionization stages

element_ion_stage_indices = []

for groupname in fin['/zonedata/0'].iterkeys():
    if (groupname[0] == 'Z'):
        elements.append(str(groupname))
        ion_stage_indices = []
        max_ion_stages = len(fin['/zonedata/0/' + str(groupname) + '/ion_fraction'] )
        sample_ion_fractions = np.array((fin['/zonedata/0/' + str(groupname) + '/ion_fraction'] ))
        for ion_stage in range(max_ion_stages):
            if (sample_ion_fractions[ion_stage] > -1):
                ion_stage_indices.append(ion_stage)
        element_ion_stage_indices.append(ion_stage_indices)

n_elements = len(elements)

# Assemble data container
state_array = []
for element_index in range(n_elements):

    state_array.append( np.zeros((n_blocks,n_zones,len(element_ion_stage_indices[element_index]))))


### Read in data ###
for block_index in range(len(filenames)):
    print "Reading block %d" % block_index
    for i in range(len(filenames[block_index])):
        fin = h5py.File(filenames[block_index][i],'r')
        for z_index in range(n_zones):
            name = '/zonedata/' + str(z_index) + '/'
            for element_index in range(n_elements):
                for ion_stage_index in element_ion_stage_indices[element_index]:
                    state_array[element_index][block_index,z_index,ion_stage_index] += np.array(fin[name + str(elements[element_index]) + '/ion_fraction'])[ion_stage_index] / len(filenames[block_index])

### plotting ###

print "starting to plot data"
for element_index in range(n_elements):
    alpha_value= 0
    for block_index in range(n_blocks):
        alpha_value += 1./(n_blocks)
        color_index = 0
        #for ion_stage in range(n_ionization_stages[element_index]):
        for ion_stage in element_ion_stage_indices[element_index]:
            if (block_index == n_blocks - 1):
                this_label = str(ion_stage+1)
            else:
                this_label = '_nolegend_'
            plt.plot(np.log10(state_array[element_index][block_index,::,ion_stage]),label=this_label,alpha=alpha_value,c = cm.jet(int(color_index * 255./float( len(element_ion_stage_indices[element_index]) - 1. ))))
            color_index += 1

    plt.suptitle(elements[element_index] + ' ion fraction')
    leg = plt.legend()
    leg.draggable(True)
    plt.xlabel("zone number")
    plt.ylabel("log10(occupation fraction)")
    plt.savefig(elements[element_index] + '_ion_fraction.pdf')
    plt.show()
    plt.close()



