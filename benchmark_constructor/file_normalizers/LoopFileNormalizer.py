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
    cmd += '\n' 
    
    cmd += 'hide all\n'
    cmd += 'show cartoon\n'
    cmd += 'color magenta, loops and name c*\n' 
    
    with open(script_path, 'w') as f:
        f.write(cmd)

  def normalize_adjacent_loop_pairs(self, loop_path, adjacent_loop_pair_set):
    with open(loop_path, 'w') as f:
      for lp in adjacent_loop_pair_set:
        f.write('LOOP {0} {1} {2} 1\nLOOP {3} {4} {5} 1\n\n'.format(lp[0].begin,
                 lp[0].end, lp[0].end, lp[1].begin, lp[1].end, lp[1].end))

  def apply(self, info_dict):
    for structure_dict in info_dict['candidate_list']:
      d = os.path.dirname(structure_dict['path']) 
      
      if 'candidate_loop_list' in structure_dict.keys():
        nl = '.'.join([structure_dict['name'], 'loop'])
        ns = structure_dict['name'] + '_select_loop.pml'
        self.normalize_one_file(os.path.join(d, nl), os.path.join(d, ns),
                                structure_dict['candidate_loop_list'])
      
      if 'adjacent_loop_pair_set' in structure_dict.keys():
        nlp = structure_dict['name'] + '_adjacent_pairs.loop'
        self.normalize_adjacent_loop_pairs(os.path.join(d, nlp), structure_dict['adjacent_loop_pair_set'])

