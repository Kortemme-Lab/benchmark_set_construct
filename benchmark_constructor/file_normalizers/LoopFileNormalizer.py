import os

from .FileNormalizer import FileNormalizer

class LoopFileNormalizer(FileNormalizer):
  '''LoopFileNormalizer creates Rosetta loop files based on the
     candidate_loop_list of structures. Also create a pymol script
     file for selecting these loops.
  '''
  def __init__(self):
    pass

  def normalize_one_file(self, loop_path, script_path, candidate_loop_list):
    with open(loop_path, 'w') as f:
      for loop in candidate_loop_list:
        f.write('LOOP {0} {1} {2} 1\n'.format(loop.begin, loop.end, loop.end))

    cmd = 'select loops,'
    for loop in candidate_loop_list:
      cmd += ' res {0}-{1} and chain {2}'.format(loop.begin, loop.end, loop.chain)
    
    with open(script_path, 'w') as f:
        f.write(cmd)

  def apply(self, info_dict):
    for structure_dict in info_dict['candidate_list']:
      d = os.path.dirname(structure_dict['path']) 
      nl = '.'.join([structure_dict['name'], 'loop'])
      ns = structure_dict['name'] + '_select_loop.pml'
      
      if 'candidate_loop_list' in structure_dict.keys():
        self.normalize_one_file(os.path.join(d, nl), os.path.join(d, ns),
                                structure_dict['candidate_loop_list'])
