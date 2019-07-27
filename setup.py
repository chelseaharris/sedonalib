from setuptools import setup, find_packages

setup(name='sedonalib',
      version='1.0.0',
      description='Awesome Sedona python library',
      url='https://github.com/chelseaharris/sedonalib',
      author='Chelsea Harris & co.',
      author_email='Chelsea email',
      license='whatever, e.g. BSD',
      packages=find_packages(),
      package_data={"sedonalib": ["analysis/*", "analysis/lightcurve/*",
                                  "data/*", "data/atomic_data/*", "data/lightcurve_filters/*",
                                  "io/*", "io/format_input/*",
                                  "loaders/*", "loaders/grids/*", "loaders/spectra/*",
                                  "plot/*"]},
      install_requires=['numpy', 'scipy', 'matplotlib==2.1.0'],
      zip_safe=False)
