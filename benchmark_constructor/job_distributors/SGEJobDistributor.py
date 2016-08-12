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
    
    qsub_command = ['qsub',
                    '-cwd',
                    '-N', self.script_name,
                    '-t', '1-{0}'.format(num_jobs),
                    '-l h_rt={0}'.format(time),
                    '-l mem_free={0}G'.format(mem_free_GB),
                    '-l scrath={0}G'.format(scratch_space_GB),
                    self.script_name,
                    data_set_path,
                    ] + self.script_arguments
    
    subprocess.check_call(qsub_command) 
