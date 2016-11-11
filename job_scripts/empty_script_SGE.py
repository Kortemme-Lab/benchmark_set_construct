#$ -S /netapp/home/xingjiepan/.local/bin/python3

'''
Empty script for debugging on SGE
'''

import os
import sys; sys.path.append(os.getcwd())

import benchmark_constructor as BC


if __name__ == '__main__':

	print(sys.version)
	print(os.getcwd())
	print("I'm doing nothing :P")
