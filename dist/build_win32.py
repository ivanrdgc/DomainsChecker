#!/usr/bin/python3

import distutils.core, py2exe

distutils.core.setup(console = [{'script': '../app.py'}])
distutils.core.setup(windows = [{'script': '../gtkapp.py'}])
