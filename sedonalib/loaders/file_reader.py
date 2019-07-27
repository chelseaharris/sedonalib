#
# Authors: Chelsea Harris
# Date 2018-12-05
#
# Purpose: 
# These functions will understand how to give a grid or specrum
# what it needs from a given Sedona output accounting for the Sedona
# version and file type
import numpy as np

class SimReader(object):
    def __init__(self):
        self.data = None


    def open(self, filename):
        """
        Open the file and store its contents 
        """
        with open(filename,'r') as rf:
            self.data = rf.readlines()


    def pull_one(self,field):
        """
        Retrieves an array for a single field
        """
        pass

    def pull_these(self, fields):
        """
        Returns a tuple of arrays corresponding to the fields listed
        """
        pass
    
    def pull_all(self):
        """
        Returns all the data as a tuple, in order corresponding to
        self.list_fields()
        """
        pass

    def list_fields(self):
        """
        Returns a list of available field specifiers.
        """
        pass

    def count_fields(self):
        """
        Tells you how many fields there are.
        """
        pass



class HDF5Reader(SimReader):
    h5py = __import__('h5py')

    def __init__(self):
        SimReader.__init__(self)

    def open(self, filename):
        self.data = self.h5py.File(filename,'r')

    def pull_one(self,field):
        if field in list(self.data.keys()):
            return np.array(self.data[field], dtype=self.data[field].dtype)
        else:
            print('Field \'{}\' does not exist.'.format(field))
            print('Available fields:', self.list_fields())
            return np.empty(0)
        
    def pull_these(self, fields):
        output = []
        for field in fields:
            output.append(self.pull_one(field))
        return output

    def pull_all(self):
        output = []
        for field in self.list_fields():
            output.append(np.array(self.data[field]))
        return output

    def count_fields(self):
        return len(self.data.keys())

    def list_fields(self):
        return list(self.data.keys())


def choose_reader(filename):
    file_type = filename.split('.')[-1]
    if file_type in ('h5','hdf5'):
        return HDF5Reader()
    else:
        return SimReader()
