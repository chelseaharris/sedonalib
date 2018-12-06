import sys
sys.path.append('..')
import plot.grid as gplt

def test_grid_plotting():
    test_file = 'example_output/SNIa/weizmann_toy_hiNi/spectrum_final.h5'
    gplt.plot_grid(test_file)


if __name__=='__main__':
    test_grid_plotting()
