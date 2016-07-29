#!/usr/bin/env python3.5
'''
Install dependencies for benchmark_set_construct
'''

import subprocess


def pip_install(package):
  subprocess.check_call(['pip3.5', 'install', package, '--user'])


if __name__ == '__main__':
  

  # Install biopython

  try:
    import numpy
  except ImportError:
    pip_install('numpy')

  try:
    import Bio
  except ImportError:
    pip_install('biopython')

  # Install docopt

  try:
    import docopt
  except ImportError:
    pip_install('docopt')
