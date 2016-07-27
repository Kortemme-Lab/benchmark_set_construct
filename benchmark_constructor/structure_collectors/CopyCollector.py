import os
import shutil

from .StructureCollector import StructureCollector


class CopyCollector(StructureCollector):
  '''CopyCollector simply copy all pdb files under a directory
      into the dataset directory
  '''
  def __init__(self, source_dir, target_dir):
    self.source_dir = source_dir
    self.target_dir = target_dir

  def apply(self):
    pdb_files = [ f for f in os.listdir(self.source_dir) if f.endswith('.pdb') ]
    
    for f in pdb_files:
      os.makedirs( os.path.join(self.target_dir, f[0:-4]) )
      shutil.copyfile( os.path.join(self.source_dir, f), 
                       os.path.join(self.target_dir, f[0:-4], f) )

    return [ {'name':f[0:-4], 'path':os.path.join(self.target_dir, f[0:-4], f)} for f in pdb_files ]
