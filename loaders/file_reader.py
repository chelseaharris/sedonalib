#
# Authors: Chelsea Harris
# Date 2018-12-05
#
# Purpose: 
# These functions will understand how to give a grid or specrum
# what it needs from a given Sedona output accounting for the Sedona
# version and file type

class SimReader(object):

  def open_file(self):
    """
    Open the file and store its contents 
    """

  def pull(self,field):
    """
    Retrieves the information specified by field from the file.
    """
    return 0

def choose_reader(filename, type=''):
  # Set type if not yet set
  if type=='':
    Types = {'h5':'HDF5', 'dat':'ASCII'}
    
    handle = filename.split('.')[-1]
    if handle not in Types.keys():
        print('Cannot load simulation output: Unknown file type.')
        return 1
    else:
        type = Types[handle]

  if file_type=='HDF5':
      return H5Reader(filename)
  if file_type=='ASCII':
      return TableReader(filename)
