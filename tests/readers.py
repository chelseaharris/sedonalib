import sys
sys.path.append('..')
import loaders.file_reader as rd



def test_hdf5_reader():
    test_file = 'example_output/SNIa/weizmann_toy_hiNi/spectrum_final.h5'

    butler = rd.SimReader() 
    print("Hello, I'm an {}, here to assist you.".format(repr(type(butler))))

    butler = rd.HDF5Reader()
    print("Hello, I'm an {}, here to assist you.".format(repr(type(butler))))

    butler.open(test_file)

    Lnu = butler.pull_one('Lnu')
    print('Lnu shape:',Lnu.shape)
    nu, time = butler.pull_these(('nu','time'))
    print('nu shape:',nu.shape)
    print('time shape:',time.shape)
    all = butler.pull_all()
    print(len(all))
    

def main():
    test_hdf5_reader()


if __name__=='__main__': main()
