import os
from setuptools import setup, find_packages

def getversion():
    """Reads version from VERSION file"""
    with open(os.path.join(os.path.dirname(__file__), 'iprPy', 'VERSION')) as f:
        return f.read().strip()

def getreadme():
    with open('README.rst') as readme_file:
        return readme_file.read()
   
setup(name = 'iprPy',
      version = getversion(),
      description = 'Interatomic Potential Repository Python Property Calculations and Tools',
      long_description = getreadme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Physics'
      ],
      keywords = [
        'atom', 
        'atomic', 
        'atomistic', 
        'molecular dynamics', 
        'high-throughput', 
        'interatomic potential',
      ], 
      url = 'https://github.com/usnistgov/iprPy',
      author = 'Lucas Hale',
      author_email = 'lucas.hale@nist.gov',
      packages = find_packages(),
      install_requires = [
        'xmltodict',
        'DataModelDict',
        'numpy', 
        'matplotlib',
        'scipy',
        'pandas',
        'numericalunits',
        'atomman>=1.2.0',
        'requests',
      ],
      package_data={'': ['*']},
      zip_safe = False)