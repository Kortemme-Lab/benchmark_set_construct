#!/usr/bin/env python3

import subprocess

import benchmark_constructor as BC


if __name__ == '__main__':
  
  # Create a new data set
  data_set_path = BC.DataController.create_new_data_set('testSet')
  
  ### DEBUG: just run the test script
  subprocess.check_call(['job_scripts/test.py', data_set_path])
