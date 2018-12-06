import ..file_reader as fread

class Grid(object):
    """
    Stores information from the grid files, about the zone properties
    needed for plotting.
    """
    def __init__(self, filename):
        """
        D-dimensional grid 
          N zones in 1st dimension
          M ...      2nd ...
          Q ...      3rd ...
        R atomic species modeled, 
        """
        
        assistant = fread.choose_reader(filename)

        assistant.open(filename)
    
        A, Z, rho, temp, comp, dr = assistant.pull_these(('A','Z','rho','temp','comp','dr'))
        # right now the species fractions are in an array of shape
        # list(rho.shape)+[num_species]
        # to do array math, need it to be
        # [num_species] + list(rho.shape)
        comp = np.moveaxis(comp, (0,1,2), (2,0,1))

        #member variable         description            total size
        self.A = A              # atomic weights       (R)
        self.Z = Z              # atomic numbers       (R)
        self.rho = rho          # mass density         (N x M x Q)
        self.temp = temp        # temperature          (N x M x Q)
        self.comp = comp        # composition          (RxNxMxQ)
        self.num_dims = len(dr) # number of dimensions (D)
        self.num_zones = rho.shape # number of zones per dimension 
        self.reader = assistant # file reader 

    # Calculate per-zone quantities
    def calc_zone_volume(self):
        """
        This function needs to return an array of zone volumes (`zone_volumes`)
        that is the appropriate shape such that
           zone_volumes * self.rho 
        gives an array shaped like self.rho containing all zone masses
        """
        pass

    def calc_zone_mass(self):
        return self.calc_zone_volume()*self.rho

    def calc_zone_species_mass(self):
        return self.calc_zone_mass() * self.comp

    # Calculate global quantities
    def calc_total_mass(self):
        return np.sum(self.calc_zone_mass())

    def calc_total_species_mass(self):
        """
        returns an R-length array of the total mass per species
        """
        return np.sum(self.calc_zone_species_mass, axis=tuple(range(1,self.num_dims)))

    def calc_total_kinetic_energy(self):
        pass


class CylindricalGrid(Grid):
    def __init__(self, filename):
        Grid.__init__(self, filename)
        
        self.v = np.empty([2]+self.rho.shape)
        self.v[0] = self.assistant.pull_one('vx')
        self.v[1] = self.assistant.pull_one('vz')

    def calc_zone_volume(self):
        x = self.dr[0]*np.arange(0.5, self.num_zones[0]+0.5)
        vols = (2*np.pi*x)*np.prod(self.dr)
        # denote: n, m = self.num_zones
        # vols has shape (n,)
        # rho has shape (n,m)
        # in order to execute vols*rho, we need vols in shape (n,1)
        return vols.reshape((vols.size,1))

    def calc_total_kinetic_energy(self):
        v_sq = np.sum(self.v**2, axis=0)
        return np.sum( 0.5*self.calc_zone_mass()*v_sq )


class Cartesian3dGrid(Grid):
    def __init__(self, filename):
        Grid.__init__(self, filename)
        
        self.v = np.empty([3]+self.rho.shape)
        self.v[0] = self.assistant.pull_one('vx')
        self.v[1] = self.assistant.pull_one('vy')
        self.v[2] = self.assistant.pull_one('vz')

    def calc_zone_volume(self):
        # volume is a uniform scalar
        vols = np.prod(self.dr)
        return vols

    def calc_total_kinetic_energy(self):
        v_sq = np.sum(self.v**2, axis=0)
        return np.sum( 0.5*self.calc_zone_mass()*v_sq )
  
  
        

class RadGrid(Grid):
    """
    A grid that stored radiation properties
    """
  

    @classmethod
    def load(filename):
  
        num_dims = len(rho.shape)
        v = np.zeros([num_dims]+list(rho.shape))
        v_fields = ('vx','vy','vz')
        for i in range(num_dims):
            v[i] = assistant.pull( v_fields[i] )
    
        return Grid(A, Z, rho, temp, v, comp)


