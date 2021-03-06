import Bio.PDB as PDB

from .SecondaryStructure import find_secondary_structures 
from .SecondaryStructure import SecondaryStructure 
from .metric import residue_group_distance

class Loop(SecondaryStructure):
  '''This is a simple class for a loop on a protein'''
  def __init__(self, begin, end, chain='A', model=0):
    self.type = 'Loop'
    self.begin = begin
    self.end = end
    self.chain = chain
    self.model = model

def find_all_loops(pdb_file):
  '''Find all loops of a pdb_file. The DSSP program is required.'''
  return find_secondary_structures(pdb_file, 'loop', Loop)


def get_loops_in_length_range(loop_list, cutoff_low, cutoff_high):
  '''Get a list of loops whose range is in the [cutoff_low, cutoff_high]'''
  return [ loop for loop in loop_list if loop.end - loop.begin + 1 >= cutoff_low \
                                         and loop.end - loop.begin + 1 <= cutoff_high ]
  
  
def loop_distance(loop1, loop2, structure):
  '''Calculate the distance between two loops'''
  return residue_group_distance(loop1.get_res_list(structure),
                                loop2.get_res_list(structure),
                                heavy_only=True)
