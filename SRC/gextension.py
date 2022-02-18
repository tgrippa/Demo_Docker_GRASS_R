#!/usr/bin/env python

"""
Functions that check if add-on is installed and install through g.extension if not yet installed
"""

import grass.script as gscript

def check_install_addon(addon):
	# 
	if addon not in gscript.parse_command('g.extension', flags="a"):
		gscript.run_command('g.extension', extension="%s"%addon)
		print("%s have been installed on your computer"%addon)
	else: print("%s is already installed on your computer"%addon)
