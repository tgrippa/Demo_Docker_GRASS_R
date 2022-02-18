#!/usr/bin/env python

"""
This script is used to store all configuration parameter to run the main code (jupyter notebook)

"""

import os

# Initialize dictionnaries
config_parameters = {}

## Please update the following paths according to your own configuration
config_parameters['GISBASE'] = '/usr/lib/grass78'
config_parameters['PYTHONLIB'] = '/usr/bin/python3'

## The following parameters should not be changed  
config_parameters['gisdb'] = os.path.join(os.environ['HOME'], 'GRASSDATA') # path to the GRASSDATA folder
config_parameters['location'] = 'nc_spm_08_grass7'
config_parameters['permanent_mapset'] = 'PERMANENT' # name of the permanent mapset
config_parameters['locationepsg'] = '3358' #  EPSG code of the location
