import os
import subprocess

from .FileNormalizer import UpdatePDBNormalizer

class PymolCleanPDBNormalizer(UpdatePDBNormalizer):
  '''Clean the PDB file with PyMol'''
  def __init__(self):
    pass

  def apply(self, info_dict):
    
    for structure_dict in info_dict['candidate_list']:
      
      script_path = os.path.join(os.path.dirname(structure_dict['path']),
                                 'pymol_pdb_clean.pml')
      
      new_pdb = os.path.join(os.path.dirname(structure_dict['path']),
                             structure_dict['name'] + '_cleaned.pdb')
      
      script = ['load {0}'.format(structure_dict['path']),
                'remove het',
                'save {0}'.format(new_pdb),
              ]

      with open(script_path, 'w') as f:
        f.write('\n'.join(script))

      
      subprocess.check_call(['pymol', '-c', script_path])

      self.update_pdb(new_pdb, structure_dict['path'])

      os.remove(script_path)
