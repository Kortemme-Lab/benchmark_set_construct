import Bio.PDB as PDB

from .Filter import Filter
from .utilities.Loop import Loop
from .utilities.Loop import find_all_loops
from .utilities.Loop import get_long_loops
from .utilities.Loop import loop_distance
from .utilities.Crystal import get_crystal_contact_residues 

class LoopFilter(Filter):
  '''Base class of filters that consider properties of loops'''
  def __init__(self):
    pass
    
  def get_loops(self, info_dict, refresh=False):
    '''Find all loops of a structure. If there is no candidate_loop_list, make the new
       found loop_list canditate
    '''
    # Iterate through a copy of the list, because the list might be modified
    for structure_dict in info_dict['candidate_list'][:]:
      if 'loop_list' not in structure_dict.keys() or refresh:
        structure_dict['loop_list'] = find_all_loops(structure_dict['path'])
      
      if 'candidate_loop_list' not in structure_dict.keys() or refresh:
        structure_dict['candidate_loop_list'] = structure_dict['loop_list']


class LoopModelChainFilter(LoopFilter):
  '''LoopModelChainFilter filters out structures that don't have loops in given model
     and chain. It also removes loops of other models and chains from the candidate_loop_list.
  '''
  def __init__(self, model=0, chain='A'):
    self.model=model
    self.chain=chain

  def apply(self, info_dict):
    self.get_loops(info_dict)

    # Iterate through a copy of the list, because the list might be modified
    for structure_dict in info_dict['candidate_list'][:]:
      selected_loops = []
      for loop in structure_dict['candidate_loop_list']:
        if loop.model == self.model and loop.chain == self.chain:
          selected_loops.append(loop)
      
      if len(selected_loops) == 0:
        self.remove_structure(info_dict, structure_dict)
      else:
        structure_dict['candidate_loop_list'] = selected_loops


class LoopLengthFilter(LoopFilter):
  '''LoopLengthFilter filters out structures that don't have loops
     longer than a cutoff. Then remove short loops from the candidate_loop_list.
     If chop=True, chop the loops into loops with length cutoff.
  '''
  def __init__(self, cutoff, chop=False):
    self.cutoff = cutoff
    self.chop = chop

  def apply(self, info_dict):
    self.get_loops(info_dict)

    # Iterate through a copy of the list, because the list might be modified
    for structure_dict in info_dict['candidate_list'][:]:
      long_loops = get_long_loops(structure_dict['candidate_loop_list'], self.cutoff)
      
      # Chop up loops if required
      
      selected_loops = []
      if self.chop:
        for loop in long_loops:
          selected_loops += loop.chop_up(self.cutoff)
      else:
        selected_loops = long_loops
      
      if len(selected_loops) == 0:
        self.remove_structure(info_dict, structure_dict)
      else:
        structure_dict['candidate_loop_list'] = selected_loops
        
        
class LoopCrystalContactFilter(LoopFilter):
  '''LoopCrystalContactFilter filters out structures that don't have loops
     which don't contact asymmetric units. Loops in the candidate_loop_list are
     splited if there are residues in the middle of loops have contacts.
  '''
  def __init__(self, cutoff, model=0, chain_list=['A'], pymol_bin='pymol'):
    self.cutoff = cutoff
    self.model = model
    self.chain_list = chain_list
    self.pymol_bin = pymol_bin

  def apply(self, info_dict):
    self.get_loops(info_dict)

    # Iterate through a copy of the list, because the list might be modified
    for structure_dict in info_dict['candidate_list'][:]:
      # Initialize the crystal_contact_res_set if necessary
      
      if 'crystal_contact_res_set' not in structure_dict.keys():
        structure_dict['crystal_contact_res_set'] = get_crystal_contact_residues(structure_dict['path'],
                                                      self.cutoff, model=self.model, chain_list=self.chain_list,
                                                      pymol_bin=self.pymol_bin)
      
      # Split loops with contacts
      
      new_loop_list = []
      for loop in structure_dict['candidate_loop_list']:
        i = loop.begin
        
        while i <= loop.end:
          if (loop.chain, i) in structure_dict['crystal_contact_res_set']:
            i += 1
            continue
          begin = i

          while i+1 <= loop.end and (loop.chain, i+1) not in structure_dict['crystal_contact_res_set']:
            i += 1

          new_loop_list.append(Loop(begin, i, loop.chain, loop.model))
          i += 1

      # Filter structures
      
      if len(new_loop_list) == 0:
        self.remove_structure(info_dict, structure_dict)
      else:
        structure_dict['candidate_loop_list'] = new_loop_list


class MultipleLoopFilter(LoopFilter):
  '''MultipleLoopFilter select structures that have adjacent loops within
     a cutoff.
  '''
  def __init__(self, cutoff, sequence_separation=5):
    self.cutoff = cutoff
    self.sequence_separation = sequence_separation

  def apply(self, info_dict):
    self.get_loops(info_dict)

    parser = PDB.PDBParser()

    # Iterate through a copy of the list, because the list might be modified
    for structure_dict in info_dict['candidate_list'][:]:
      structure = parser.get_structure('', structure_dict['path'])

      # Create a set to store adjacent loop pairs
      
      structure_dict['adjacent_loop_pair_set'] = set()

      # Find all loops that have close contact to other loops

      selected_loops = []
      for loop1 in structure_dict['candidate_loop_list']:
        for loop2 in structure_dict['candidate_loop_list']:
          if loop1.connected(loop2, self.sequence_separation) or loop1.model != loop2.model:
            continue

          if loop_distance(loop1, loop2, structure) <= self.cutoff:
            if loop1 not in selected_loops:
              selected_loops.append(loop1) # Here only add loop1 so that the order of loops in the list is kept
            if loop1 < loop2:
              structure_dict['adjacent_loop_pair_set'].add((loop1, loop2))
            
      if len(selected_loops) == 0:
        self.remove_structure(info_dict, structure_dict)
      else:
        structure_dict['candidate_loop_list'] = selected_loops 
