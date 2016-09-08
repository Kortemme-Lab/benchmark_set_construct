import os
import shutil

from .FileNormalizer import FileNormalizer

class MakeNativeCopyNormalizer(FileNormalizer):
  '''Make a copy of the PDB file and mark it as the native structure.'''
  def __init__(self):
    pass

  def apply(self, info_dict):
    for structure_dict in info_dict['candidate_list']:
      native_name = os.path.join(os.path.dirname(structure_dict['path']),
                        structure_dict['name'] + '_native.pdb')
      shutil.copyfile(structure_dict['path'], native_name) 
                        
