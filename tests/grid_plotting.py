from sedonalib.plot import plot_grid

def test_grid_plotting():
    test_file = 'example_output/SNIa/weizmann_toy_hiNi/spectrum_final.h5'
    plot_grid(test_file)


if __name__=='__main__':
    test_grid_plotting()
