import os

from .FileNormalizer import FileNormalizer

class LoopFileNormalizer(FileNormalizer):
  '''LoopFileNormalizer creates Rosetta loop files based on the
     candidate_loop_list of structures.
  '''
  def __init__(self):
    pass

  def normalize_one_file(self, path, candidate_loop_list):
    with open(path, 'w') as f:
      for loop in candidate_loop_list:
        f.write('LOOP {0} {1} {2} 1\n'.format(loop.begin, loop.end, loop.end))

  def apply(self, info_dict):
    for structure_dict in info_dict['candidate_list']:
      d = os.path.dirname(structure_dict['path']) 
      n = '.'.join([structure_dict['name'], 'loop'])
      
      self.normalize_one_file(os.path.join(d, n), structure_dict['candidate_loop_list'])
