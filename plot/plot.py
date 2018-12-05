#
# Authors: Dan Kasen, Chelsea Harris
# Date: 2018-12-5          
# 
# Purpose: Plot Sedona `plot` output files

import matplotlib.pyplot as plt
import numpy as np
import h5py

cMsun = 1.99e33

def load_model(filename):
  """
  Read in the model data. This needs to be abstracted out of the code.
  """
  data = h5py.File(filename,'r')
  ndims = len(  np.array(data['rho']).shape )
  return ndims, data
    

def get_props_1d(data):
  print('No plotting functionality for 1D models.')
  return 0


def get_props_2d(data):
  """
  This function should be abstracted out of the code
  """
  Z    = np.array(data['Z'])
  A    = np.array(data['A'])
  rho  = np.array(data['rho'],dtype='d')
  temp = np.array(data['temp'],dtype='d')
  comp = np.array(data['comp'],dtype='d')
  dr   = np.array(data['dr'],dtype='d')

  vx = np.array(data['vx'],dtype='d')
  vz = np.array(data['vz'],dtype='d')

  return Z, A, rho, temp, comp, dr, vx, vz


def get_props_3d(data):
  """
  This function should be abstracted out of the code
  """
  Z    = np.array(data['Z'])
  A    = np.array(data['A'])
  rho  = np.array(data['rho'],dtype='d')
  temp = np.array(data['temp'],dtype='d')
  comp = np.array(data['comp'],dtype='d')
  dr   = np.array(data['dr'],dtype='d')

  vx = np.array(data['vx'],dtype='d')
  vy = np.array(data['vz'],dtype='d')
  vz = np.array(data['vz'],dtype='d')
  rmin = np.array(dta['rmin'],dtype='d')

  return Z, A, rho, temp, comp, dr, vx, vy, vz, rmin


def plot_1d(data):
  print('No plotting functionality for 1D models.')
  return 0


def plot_2d(data, verbose=False):
  """
  Assumes cylindrical grid
  """
  Z, A, rho, temp, comp, dr vx, vz = get_props_2d(data)

  # calculate total zone speeds, squared
  v_squared = vx**2 + vz**2

  # calculate zone volumes
  xsize, zsize = rho.shape
  x_center = dr[0] * np.arange(0.5, xsize+0.5)
  z_center = dr[1] * np.arange(0.5, zsize+0.5)
  zone_volume = (2*np.pi*x)*dr[0]*dr[1]

  # Calculate model integrated quantities
  zone_mass = (zone_volume*rho.T).T # has shape of rho
  mass = np.sum(zone_mass)
  # need to reorder the axes of comp to do array math
  comp_multorder = np.moveaxis(comp, (0,1,2), (2,0,1))
  species_mass = np.sum(zone_mass*comp_multorder, axis=(1,2))
  if len(species_mass)!=len(Z):
    print('OMG Chelsea stop trying to be clever and fix your array shapes.')
  # I think this can be replaced by
  # np.sum(zone_volume.dot(0.5*rho*v_squared))
  kin_energy = np.sum(zone_volume*0.5*(rho*v_squared).T)

  if verbose:
  	print('-----------------------------------------------------------')
  	print('dimensions; (nx,nz) = ({},{})'.format(xsize, zsize))
  	print ('zonesizes:  (dx,dz) = ({0:.4e}, {1:.4e})'.format(dr[0],dr[1]))
  	print('mass = {0:.4e} grams ({1:.4e} M_sun)'.format(mass,mass/cMsun))
  	print('E_kin  = {0:.4e}  ergs'.format(kin_energy))
  	for k in range(len(Z)):
  		print 'elem ' +str(Z[k]) + '.' + str(A[k]),
  		print(': mass = {0:.4e} grams ({1:.4e} M_sun)'.format(species_mass[k],species_mass[k]/cMsun))
  	print('-----------------------------------------------------------')
  

  plt.matshow(np.log10(rho.T))
  plt.colorbar()
  plt.title('log$_{10}$ density')

  for prop, label in zip((temp, vx, vz), ('temperature','x-velocity', 'z-velocity')):
    plt.figure()
    plt.matshow(prop.T)
    plt.colorbar()
    plt.title(label)

  for k in range(len(Z)):
    plt.figure()
    plt.matshow( (comp[:,:,k]).T )
    plt.colorbar()
    plt.title('mass fraction of Z = {}.{}'.format(Z[k],A[k]))

  plt.show()
  

def plot_3d(data):
  """
  Assumes Cartesian grid
  """
  Z, A, rho, temp, comp, dr, vx, vy, vz, rmin = get_props_3d(data)

  xsize, ysize, zsize = rho.shape

  # zones are cubes
  zone_volume = dr[0]*dr[1]*dr[2]
  v_squared = vx**2 + vy**2 + vz**2

  # calculate integrated quantities
  mass = np.sum(rho*zone_volume)
  kin_energy = np.sum(0.5*rho*v_squared*zone_volume)

  # can do array math but only if composition matrix has different shape
  comp_multorder = np.moveaxis(comp, (0,1,2,3), (3,0,1,2))
  species_mass = np.sum(comp_multorder*rho*zone_volume, axis=(1,2,3))
  if len(species_mass)!=len(Z): 
    print('Chelsea, why did you think you could handle crazy 4-D array math? Fix this.')


  print('-----------------------------------------------------------')
  print('dimensions; (nx,ny,nz) = ({},{},{})'.format(xsize, ysize, zsize))
  print ('zonesizes:  (dx,dy,dz) = ({0:.4e}, {1:.4e},{2:.4e})'.format(dr[0],dr[1],dr[2]))
  print ('min_pos:    (x0,y0,z0) = ({0:.4e}, {1:.4e},{2:.4e})'.format(rmin[0],rmin[1],rmin[2]))
  print('mass = {0:.4e} grams ({1:.4e} M_sun)'.format(mass,mass/cMsun))
  for k in range(len(Z)):
  	print('element {}.{}'.format(Z[k],A[k]))
  	print(': mass = {0:.4e} grams ({1:.4e} M_sun)'.format(cmass[k],cmass[k]/cMsun))
  print('E_kin   = {0:.4e}  ergs'.format(kin_energy))
  print('-----------------------------------------------------------')
  
  plt.matshow(np.log10(rho[:,:,nx//2]))
  plt.colorbar()
  plt.title('log10 density x-y plane')
  
  plt.matshow(np.log10(rho[:,nx//2,:]))
  plt.colorbar()
  plt.title('log10 density x-z plane')
  
  plt.matshow(np.log10(rho[nx//2,:,:]))
  plt.colorbar()
  plt.title('log10 density y-z plane')

  plt.show()


def plot(filename):
  ndims, props = load_model(filename)

  if   ndims==1: plot_1d(*props)
  elif ndims==2: plot_2d(*props)
  elif ndims==3: plot_3d(*props)
  else: 
      print('Twilight Zone plotting not yet implemented.')

plt.ion()
