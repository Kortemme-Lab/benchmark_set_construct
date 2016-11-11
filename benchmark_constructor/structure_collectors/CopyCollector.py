import os
import shutil
import math

from .StructureCollector import StructureCollector


class CopyCollector(StructureCollector):
  '''CopyCollector simply copy all pdb files under a directory
      into the dataset directory
  '''
  def __init__(self, source_dir, target_dir, num_jobs=1, job_id=1):
    self.source_dir = source_dir
    self.target_dir = target_dir
    self.num_jobs = num_jobs
    self.job_id = job_id

  def apply(self):
    pdb_files = sorted([ f for f in os.listdir(self.source_dir) if f.endswith('.pdb') ])
    
    file_per_job = int(math.ceil(len(pdb_files) / self.num_jobs))
    start = (self.job_id - 1) * file_per_job
    stop = self.job_id * file_per_job

    my_pdb_files = pdb_files[start:stop]

    for f in my_pdb_files:
      os.makedirs( os.path.join(self.target_dir, f[0:-4]) )
      shutil.copyfile( os.path.join(self.source_dir, f), 
                       os.path.join(self.target_dir, f[0:-4], f) )

    return [ {'name':f[0:-4], 'path':os.path.join(self.target_dir, f[0:-4], f)} for f in my_pdb_files ]
