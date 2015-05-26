#!/usr/bin/python3

import distutils.core, py2exe, sys, shutil, os.path

sources_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
build_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'win32')

shutil.rmtree(build_path, True)

sys.path.append(sources_path)
sys.argv.append('py2exe')
distutils.core.setup(options = {'py2exe': {'dist_dir': build_path, 'includes': 'common'}}, console = [{'script': os.path.join(sources_path, 'app.py')}])
distutils.core.setup(options = {'py2exe': {'dist_dir': build_path, 'includes': 'common'}}, windows = [{'script': os.path.join(sources_path, 'gtkapp.py')}])

shutil.copy2(os.path.join(sources_path, 'tld.csv'), os.path.join(build_path, 'tld.csv'))
shutil.copy2(os.path.join(sources_path, 'config.ini'), os.path.join(build_path, 'config.ini'))
