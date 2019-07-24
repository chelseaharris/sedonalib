#
# Authors: Dan Kasen, Chelsea Harris
# Date: 2018-12-5          
# 
# Purpose: Plot Sedona `plot` output files

import matplotlib.pyplot as plt
import numpy as np
import h5py

import ..loaders.grid as gload
import ..data.physical_constants as C

def plot_1d(filename):
  print('No plotting functionality for 1D models.')
  return 0


def plot_2d(filename, verbose=False):
  """
  Assumes cylindrical grid
  """
  grid = gload.CylindricalGrid(filename)

  mass = grid.calc_total_mass()
  species_mass = grid.calc_total_species_mass()

  if verbose:
  	print('-----------------------------------------------------------')
  	print('dimensions; (nx,nz) = ({},{})'.format(grid.num_zones[0], grid.num_zones[1]))
  	print ('zonesizes:  (dx,dz) = ({0:.4e}, {1:.4e})'.format(grid.dr[0],grid.dr[1]))
  	print('mass = {0:.4e} grams ({1:.4e} M_sun)'.format(mass,mass/C.M_SUN))
  	print('E_kin  = {0:.4e}  ergs'.format(grid.calc_total_kinetic_energy()))
  	for k in range(len(Z)):
  		print 'elem ' +str(Z[k]) + '.' + str(A[k]),
  		print(': mass = {0:.4e} grams ({1:.4e} M_sun)'.format(species_mass[k],species_mass[k]/C.M_SUN))
  	print('-----------------------------------------------------------')
  
  plt.matshow(np.log10(grid.rho.T))
  plt.colorbar()
  plt.title('log$_{10}$ density')

  for prop, label in zip((grid.temp, grid.v[0], grid.v[1]), ('temperature','x-velocity', 'z-velocity')):
    plt.figure()
    plt.matshow(prop.T)
    plt.colorbar()
    plt.title(label)

  for i in range(len(Z)):
    plt.figure()
    plt.matshow( (grid.comp[i]).T )
    plt.colorbar()
    plt.title('mass fraction of Z = {}.{}'.format(Z[i],A[i]))

  plt.show()
  plt.ion()


def plot_3d(filename):
  """
  Assumes Cartesian grid
  """
  grid = gload.Cartesian3dGrid(filename)

  # calculate integrated quantities
  mass = grid.calc_total_mass()
  species_mass = grid.calc_total_species_mass()
  kin_energy = grid.calc_total_kinetic_energy()

  print('-----------------------------------------------------------')
  print('dimensions; (nx,ny,nz) = ({},{},{})'.format(grid.num_zones[0], grid.num_zones[1], grid.num_zones[2]))
  print ('zonesizes:  (dx,dy,dz) = ({0:.4e}, {1:.4e},{2:.4e})'.format(grid.dr[0],grid.dr[1],grid.dr[2]))
  print ('min_pos:    (x0,y0,z0) = ({0:.4e}, {1:.4e},{2:.4e})'.format(grid.rmin[0],grid.rmin[1],grid.rmin[2]))
  print('mass = {0:.4e} grams ({1:.4e} M_sun)'.format(mass,mass/C.M_SUN))
  for k in range(len(Z)):
  	print('element {}.{}'.format(Z[k],A[k]))
  	print(': mass = {0:.4e} grams ({1:.4e} M_sun)'.format(cmass[k],cmass[k]/C.M_SUN))
  print('E_kin   = {0:.4e}  ergs'.format(kin_energy))
  print('-----------------------------------------------------------')
  
  nx = grid.num_zones[0]

  plt.matshow(np.log10(grid.rho[:,:,nx//2]))
  plt.colorbar()
  plt.title('log10 density x-y plane')
  
  plt.matshow(np.log10(grid.rho[:,nx//2,:]))
  plt.colorbar()
  plt.title('log10 density x-z plane')
  
  plt.matshow(np.log10(grid.rho[nx//2,:,:]))
  plt.colorbar()
  plt.title('log10 density y-z plane')

  plt.show()
  plt.ion()
