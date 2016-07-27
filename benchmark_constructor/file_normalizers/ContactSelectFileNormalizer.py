import os

from .FileNormalizer import FileNormalizer

class ContactSelectFileNormalizer(FileNormalizer):
  '''ContactSelectFileNormalizer creates a pymol script that selects
     residues which have contacts to asymmetric units.
  '''
  def __init__(self):
    pass
    
  def normalize_one_file(self, path, crystal_contact_res_set):
    cmd = 'select crystal_contact_res,'
    for res in crystal_contact_res_set:
      cmd += ' res {0} and chain {1}'.format(res[1], res[0])

    with open(path, 'w') as f:
      f.write(cmd)

  def apply(self, info_dict):
    for structure_dict in info_dict['candidate_list']:
      d = os.path.dirname(structure_dict['path']) 
      n = '.'.join([structure_dict['name']+'_show_crystal_contact', 'pml'])
      
      if 'crystal_contact_res_set' in structure_dict.keys():
        self.normalize_one_file(os.path.join(d, n), structure_dict['crystal_contact_res_set'])
    
        
