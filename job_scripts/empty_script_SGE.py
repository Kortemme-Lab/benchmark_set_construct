#$ -S /netapp/home/xingjiepan/.local/bin/python3

'''
Empty script for debugging on SGE
'''

import os
import sys; sys.path.append(os.getcwd())

import benchmark_constructor as BC


if __name__ == '__main__':

  os.environ['PATH'] = ':'.join(['/netapp/home/xingjiepan/.local/bin',
                                  os.environ['PATH']])

  print(sys.version)
  print(sys.path)
  print(os.getcwd())
  print(os.environ['PATH'])
  
  print("I'm doing nothing :P")
