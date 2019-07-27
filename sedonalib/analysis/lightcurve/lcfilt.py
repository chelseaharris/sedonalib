#!/usr/bin/python
#
# Author: David Khatami <dkhatami@astro.berkeley.edu>
#         Chelsea Harris
# Date: 10/4/18
#       2018-12-04
#
#
# Instructions:
# --------------
#   To run, use the command "python lcfilt.py -s <input file> -b <band1,band2,...>
#   where <input file> is the path to the spectrum.h5 file
#   and <band1,band2,...> is a list of comma-separated filters
#   
#   Example Usage: python lcfilt.py -s /Users/dkhatami/data/spectrum.h5 -b U,B,V
#       ...generates U,B,V AB magnitude light curves from the spectrum file
#   
#   For a list of filters, use "python lcfilt.py --bands"
# -------------   
#   Return: File called "lightcurve.out" in the format of
#   	Columns: 1. Time (Days) 2. Bolometric Luminosity (erg/s) 3. Bol. Mag. [4,5,...] Filter magnitudes
# 	 	Invalid elements are assigned a value of "0"
#		Floors the magnitudes to 0 if <0
# -------------
# 
# Provided filter data taken from Charlie Conroy's Flexible Stellar Population Synthesis (FSPS) Code
#  See the doc/manual.pdf in the FSPS github for how the magnitudes are defined
#

import h5py
import numpy as np
from scipy.interpolate import interp1d
from scipy import integrate as integrate

# The path here according to whatever called this module, for finding data files:
my_loc = '/'.join(__file__.split('/')[:-1])+'/'
filter_data_loc = my_loc + '../../data/lightcurve_filters/'

filter_list_fn = filter_data_loc + 'filter_list.txt'
all_filter_table_fn = filter_data_loc + 'all_filters.dat'

class Filter:

# contains the filter data and interpolation routines

    def __init__(self):
        self.Bands = {}
        self.FilterDatasets = [[]]
        with open(filter_list_fn) as f:
            for line in f:
                dat = line.split()
                self.Bands[dat[1]] = int(dat[0])

        with open(all_filter_table_fn) as f:
            for line in f:
                if line.startswith('#'):
                    if self.FilterDatasets[-1] != ():
                        self.FilterDatasets.append([])
                else:
                    stripped_line = line.strip()
                    if stripped_line:
                        self.FilterDatasets[-1].append(stripped_line.split())

    # returns the raw filter transmission curve as {Wavelength (Angstrom), Transmission}
    def getTransmission(self,filt):
        filt_idx = self.Bands[filt]
        return np.array(self.FilterDatasets[filt_idx],dtype=np.float32)

    # returns an interpolation function for the transmission T(lambda)
    # from the raw data
    def transFunc(self,filt):
        wv,f = np.transpose(self.getTransmission(filt))
        interp = interp1d(wv,f,bounds_error=False,fill_value=0.0)
        return interp
    
    # returns an interpolation function for the transmission T(nu)
    def transFunc_nu(self,filt):
        wv,f = np.transpose(self.getTransmission(filt))
        nu = 3e10/(wv/1e8)
        interp = interp1d(nu,f,bounds_error=False,fill_value=0.0)
        return interp

    # get the filter boundaries
    def filtBounds(self,filt):
        return np.min(self.getTransmission(filt)[:,0]),np.max(self.getTransmission(filt)[:,0])

    # returns the normalization for the transmission
    def getNormalization(self,filt,nu):
        sample_points = self.transFunc_nu(filt)(nu)/nu
        return integrate.trapz(sample_points,nu)      

    
    
class LightCurve:
   
# takes an input spectrum and a list of filters to convert to AB mag. light curves

 
    def __init__(self,sname):
        self.fname = sname
        self.sdat = h5py.File(sname,'r')
        self.nu = np.array(self.sdat['nu'])
        self.spec = self.sdat['Lnu']
        self.time = np.array(self.sdat['time'])
        self.filter = Filter()
       

    # returns the bolometric light curve (in erg/s) 
    def get_bolometric_lum(self):
        lum = np.zeros(self.time.size)
        dnu = np.ediff1d(self.nu,to_end=0)
        for i in range(self.time.size):
            lum[i] = np.sum(self.spec[i]*dnu)
        lum[np.where(lum==0)] = 1e-10
        return lum

   # returns the bolometric light curve (abs. magnitude) 
    def get_bolometric_mag(self):
        mags = -2.5*np.log10(self.get_bolometric_lum())+88.697425
        mags[np.where(np.isinf(mags))]=0.
        mags[np.where(mags>0)] = 0. #set minimum mag to 0
        return mags
   
   # returns the AB magnitude light curve, for a given band 
    def get_ABMag(self,band):
        lum = np.zeros(self.time.size)
        dnu = np.ediff1d(self.nu,to_end=0)
        for i in range(self.time.size):
            sample_points = np.array(self.spec[i])/self.nu*(self.filter.transFunc_nu(band)(self.nu))
            lum[i] = integrate.trapz(sample_points,x=self.nu)
        lum = lum/self.filter.getNormalization(band,self.nu) #gets Lnu(band)
        flx = lum/(4.*np.pi*(10.*3.0857e18)**2) #convert to flux at 10pc
        flx[np.where(flx==0.)] = 1e-99 #some small number so not taking log(0)
        mag = -2.5*np.log10(flx)-48.6 #get the AB magnitude
        mag[np.where(mag>0)] = 0. #set minimum mag to 0
        return mag
   
   # takes two bands and returns the color 
    def get_color(self,band1,band2):
        return self.ABMag(band1)-self.ABMag(band2)
   
   # takes a list of bands and returns their AB magnitude light curves 
    def get_lcs(self,bands):
        time_arr = self.time/(24.*3600.)
        mag_array = np.zeros((len(bands),self.time.size))
        for i in range(len(bands)):
            mag_array[i] = self.get_ABMag(bands[i])
        mag_array[np.where(np.isinf(mag_array))] = 0.
        mag_array[np.where(mag_array>0)] = 0.
        return mag_array
   
   # writes out the file to "lightcurve.out" 
    def write_bands(self,bands):
        dat_arr = np.c_[self.time/(24.*3600),self.get_bolometric_lum(),self.get_bolometric_mag(),
                                 self.get_lcs(bands).T]
        filename = "lightcurve.out"
        header_arr = "Time (Days) \t Lbol (erg/s) \t Mbol \t  {} \n All magnitudes are given in the AB Magnitude System".format('\t'.join(map(str,tuple(bands))))
        np.savetxt(filename,dat_arr,header=header_arr,fmt='%.6e')
    

def lightcurve_from_spectrum(spectrum_fn='', bands=(), out_fn='lightcurve.dat', verbose=False):
    """
    Makes the light curves in a set of photometric passbands from a
    time series of spectra.
    INPUTS
    specfile : string        path to the spectrum time series as a relative path from the current working
                             directory or as an absolute path
    bands    : string-tuple  desired photometric passbands
    """

    # We need to put an assert statement here like
    # assert slib.get_file_type(specfile) == 'HDF5'

    lc = LightCurve(spectrum_fn)
    lc.write_bands(bands)

    if verbose:
        print("Filename: {}".format(specfile))
        print("Bands: {}".format(bands))
        print("Output written to "+out_fn)



def print_avialable_bands():
    filt = Filter()
    print(', '.join(tuple(filt.Bands)))
    print('See {} for details and references.'.format(filter_list_filename))

    
