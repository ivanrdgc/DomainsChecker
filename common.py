#!/usr/bin/python3

def get_full_path(file):
	import sys, os.path

	# If compiled with py2exe
	if (hasattr(sys, 'frozen')):
		return(os.path.join(os.path.dirname(os.path.realpath(sys.executable)), file))
	else:
		return(os.path.join(os.path.dirname(os.path.realpath(__file__)), file))

def read_config():
	import configparser

	config = configparser.ConfigParser()
	config.read(get_full_path('config.ini'))
	return config['DEFAULT']
