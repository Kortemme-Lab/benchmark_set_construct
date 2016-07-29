#!/usr/bin/env python3.5
'''
Install dependencies for benchmark_set_construct
'''

import platform
import subprocess
import shutil


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

  # Download DSSP
  
  if None == shutil.which('dssp'):  

    system = platform.system()

    if system == 'Windows':
      subprocess.check_call(['wget', 'ftp://ftp.cmbi.ru.nl/pub/software/dssp/dssp-2.0.4-win32.exe'])

    else:
      subprocess.check_call(['wget', 'ftp://ftp.cmbi.ru.nl/pub/software/dssp/dssp-2.0.4-linux-i386'])

