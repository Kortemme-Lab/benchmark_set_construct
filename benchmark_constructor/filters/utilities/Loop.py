import Bio.PDB as PDB

from .Chemistry import Coarse_secondary_structure 
from .metric import residue_group_distance

class Loop:
  '''This is a simple class for a loop on a protein'''
  def __init__(self, begin, end, chain='A', model=0):
    self.begin = begin
    self.end = end
    self.chain = chain
    self.model = model

  def __repr__(self):
    s = '<Loop: begin {0}, end {1}, chain {2}, model {3}>'.format(self.begin,
          self.end, self.chain, self.model)
    return s

  def __lt__(loop2):
    if self.model < loop2.model:
      return True
    elif self.model == loop2.model:
      if self.chain < loop2.chain:
        return True
      elif self.chain == loop2.chain:
        if self.begin < loop2.begin:
          return True
        elif self.begin == loop2.begin:
          return self.end < loop2.end
        
    return False

  def get_res_list(self, structure):
    '''Get the list of residues of the loop.'''
    return [structure[self.model][self.chain][i] for i in range(self.begin, self.end+1)] 


def find_all_loops(pdb_file):
  '''Find all loops of a pdb_file. The DSSP program is required.'''
  loop_list = []
  
  parser = PDB.PDBParser()
  structure = parser.get_structure('', pdb_file)
 
  for model_id, model in enumerate(structure):
    # Calculate the secondary structures of a model with DSSP

    dssp = PDB.DSSP(model, pdb_file)
    keys = list( dssp.keys() )
    if len(keys) == 0: return loop_list

    # Get all transition points of secondary structures. If a residue is neither helix or strand, it is deemed as a part of a loop.

    transition_points = [0]
    
    for i in range(1, len(keys)):
      res_info = dssp[keys[i]]
      res_info_prev = dssp[keys[i-1]]
      
      if keys[i][0] != keys[i-1][0] \
         or keys[i][1][1] != keys[i-1][1][1] + 1 \
         or Coarse_secondary_structure(res_info[2]) != Coarse_secondary_structure(res_info_prev[2]):
         transition_points.append(i)
    
    # Get loops
    
    for i, t in enumerate(transition_points):
      ss_type = Coarse_secondary_structure( dssp[keys[t]][2] )
      if ss_type != 'loop': continue

      chain = keys[t][0]
      start = keys[t][1][1]
      end = keys[transition_points[i+1] - 1][1][1] if i < len(transition_points)-1 else keys[-1][1][1] 

      loop_list.append(Loop(start, end, chain=chain, model=model_id))

  # The best container for loops is ordered set which is not supported by official python package. So
  # use a list as container as a compromise.
  return loop_list


def get_long_loops(loop_list, cutoff):
  '''Get a list of loops that is longer or equal to a cutoff length'''
  return [ loop for loop in loop_list if loop.end - loop.begin + 1 >= cutoff ]
  
  
def loop_distance(loop1, loop2, structure):
  '''Calculate the distance between two loops'''
  return residue_group_distance(loop1.get_res_list(structure),
                                loop2.get_res_list(structure),
                                heavy_only=True)
