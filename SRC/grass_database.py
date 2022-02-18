#!/usr/bin/env python

"""
Functions for automatic check and creation of GRASS GIS database folders
"""

import os
import grass.script as gscript
import grass.script.setup as gsetup
import shutil ## Import library for file copying 
from __main__ import config_parameters


def check_gisdb(gisdb_path):
	## Automatic creation of GRASSDATA folder
	if os.path.exists(gisdb_path):
		return "GRASSDATA folder already exist" 
	else: 
		os.makedirs(gisdb_path) 
		return "GRASSDATA folder created in '%s'"%gisdb_path
		
def check_location(gisdb_path,location_name,epsg):
	## Automatic creation of GRASS location is doesn't exist
	if os.path.exists(os.path.join(gisdb_path,location_name)):
		return "Location '%s' already exist"%location_name
	else : 
		gscript.core.create_location(gisdb_path, location_name, epsg=epsg, overwrite=False)
		return "Location '%s' created"%location_name
	
def check_mapset(gisdb_path,location_name,mapset_name):
	### Automatic creation of GRASS GIS mapsets
	if os.path.exists(os.path.join(gisdb_path,location_name,"PERMANENT")):  # Check if PERMANENT mapset exists because it is needed
		if not os.path.exists(os.path.join(gisdb_path,location_name,"PERMANENT",'WIND')): # Check if PERMANENT mapset exists because it is needed
			return "WARNING: 'PERMANENT' mapset already exist, but a 'WIND' file is missing. Please solve this issue."
		else: 
			if not os.path.exists(os.path.join(gisdb_path,location_name,mapset_name)):
				os.makedirs(os.path.join(gisdb_path,location_name,mapset_name))
				shutil.copy(os.path.join(gisdb_path,location_name,'PERMANENT','WIND'),os.path.join(gisdb_path,location_name,mapset_name,'WIND'))
				return "'%s' mapset created in location '%s'"%(mapset_name,location_name)
			else:
				return "'%s' mapset already exists in location '%s'"%(mapset_name,location_name)
	else:
		return "WARNING: 'PERMANENT' mapset do not exist. Please solve this issue."

def working_mapset(gisdb_path,location_name,mapset_name):
	## Launch GRASS GIS working session in the mapset
	if os.path.exists(os.path.join(gisdb_path,location_name,mapset_name)):
		gsetup.init(os.environ['GISBASE'], gisdb_path,location_name,mapset_name)
		return "You are now working in mapset '%s/%s'"%(location_name,mapset_name)
	else: 
		return "'%s' mapset doesn't exists in '%s'"%(mapset_name,gisdb_path)
	
def launch_mapset(mapset):
    #Declare empty list that will contain the messages to return
    return_message = []
    # Check if the location exists and creates it if needed, with the CRS defined by the epsg code 
    return_message.append(check_location(config_parameters["gisdb"],config_parameters['location'],config_parameters["locationepsg"]))
    # Check if mapset exists
    return_message.append(check_mapset(config_parameters["gisdb"],config_parameters['location'],mapset))
    # Change the current working GRASS GIS session mapset
    return_message.append(working_mapset(config_parameters["gisdb"],config_parameters['location'],mapset))
    # Return
    return return_message