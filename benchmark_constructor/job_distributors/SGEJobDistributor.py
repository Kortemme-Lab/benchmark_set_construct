import os
import subprocess

from .JobDistributor import JobDistributor
from . import DataController


class SGEJobDistributor(JobDistributor):
  '''Run jobs parallel on a sun grid engine.'''
  def __init__(self, data_set_name, script_name, script_arguments=[]):
    self.data_set_name = data_set_name
    self.script_name = script_name
    self.script_arguments = script_arguments

  def run(self, num_jobs, time='1:00:00', mem_free_GB=1, scratch_space_GB=1,
          architecture='linux-x64'):
    data_set_path = DataController.create_new_data_set(self.data_set_name)
    job_output_path = os.path.join(data_set_path, "job_outputs")
    os.mkdir(job_output_path)

    qsub_command = ['qsub',
                    '-cwd',
                    '-N', self.script_name.split('/')[-1],
                    '-t', '1-{0}'.format(num_jobs),
                    '-l', 'h_rt={0}'.format(time),
                    '-l', 'mem_free={0}G'.format(mem_free_GB),
                    '-l', 'scratch={0}G'.format(scratch_space_GB),
                    '-l', 'arch=linux-x64',
                    '-o', job_output_path,
                    '-e', job_output_path,
                    self.script_name,
                    num_jobs,
                    data_set_path,
                    ] + self.script_arguments
    
    subprocess.check_call(qsub_command) 

  def set_qb3cluster_environment():
    '''Set the environment variables for the QB3 shared cluster.'''
    os.environ['PATH'] = ':'.join(['/netapp/home/xingjiepan/.local/bin', os.environ['PATH']])

    mysql_lib = '/netapp/home/kbarlow/lib/mysql-connector-c-6.1.2-linux-glibc2.5-x86_64/lib'
    try:
      os.environ['LD_LIBRARY_PATH'] = ':'.join([mysql_lib, os.environ['LD_LIBRARY_PATH']])
    except KeyError:
      os.environ['LD_LIBRARY_PATH'] = mysql_lib
