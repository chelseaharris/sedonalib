class Grid(object):
  """
  Stores information from the grid files, about the zone properties
  needed for plotting.
  """
  def __init__(self, A, Z, rho, temp, v, comp):
    """
    D-dimensional grid 
      N zones in 1st dimension
      M ...      2nd ...
      Q ...      3rd ...
    R atomic species modeled, 
    """
    # Make sure the arrays are all appropriately shaped
    assert len(A) == len(Z)
    assert rho.shape == temp.shape
    assert v.shape[0] == len(rho.shape)
    assert v.shape[1:] == rho.shape
    assert comp.shape[0] == len(A)
    assert comp.shape[1:] == rho.shape
    
    #member variable    description            total size
    self.A_ = A         # atomic weights       (R)
    self.Z_ = Z         # atomic numbers       (R)
    self.rho_ = rho     # mass density         (N x M x Q)
    self.temp_ = temp   # temperature          (N x M x Q)
    self.v_ = v         # velocity             (D x N x M x Q)
    self.comp_ = comp   # composition          (R x N x M x Q)

  @classmethod
  def load(filename):
    assistant = Reader(filename)

    A, Z, rho, temp, comp = assistant.pull(('A','Z','density','temperature','composition'))

    num_dims = len(rho.shape)
    v = np.zeros([num_dims]+list(rho.shape))
    v_fields = ('vx','vy','vz')
    for i in range(num_dims):
        v[i] = assistant.pull( v_fields[i] )

    return Grid(A, Z, rho, temp, v, comp)

  # 
  # Accessor functions
  # 
  def get_A(self):
    return self.A_

  def get_Z(self):
    return self.Z_

  def get_rho(self):
    return self.rho_
