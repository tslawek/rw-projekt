#! /usr/bin/env python

from ConfigParser import *

config_file = 'config.conf'



def read_configuration(section):
	
	cp = ConfigParser()
	cp.read(config_file)

	#options = {}
	#for i in cp.items('Parser'):
	#	options[i[0]] = i[1]
	return dict(cp.items(section))
