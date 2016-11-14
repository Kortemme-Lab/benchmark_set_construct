import os

import numpy as np
import Bio.PDB as PDB

from .utilities.metric import get_residues_nearby
from .FileNormalizer import FileNormalizer
from .FileNormalizer import UpdatePDBNormalizer

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
        f.write('LOOP {0} {1} {2} 0 1\n'.format(loop.begin, loop.end, loop.end))

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
        f.write('LOOP {0} {1} {2} 0 1\nLOOP {3} {4} {5} 0 1\n\n'.format(lp[0].begin,
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


class LoopTrimNormalizer(UpdatePDBNormalizer):
  '''LoopTrimNormalizer creates a new PDB file whose loop is replaced by a
     straight line and the side chains of residues within a cutoff from
     the loop are trimed.
  '''
  def __init__(self, cutoff):
    self.cutoff = cutoff

  def trim_one_residue(self, residue, atom_list):
    new_res = PDB.Residue.Residue(residue.get_id(), residue.get_resname(), residue.get_segid())
    
    for keep_atom in atom_list: 
      if keep_atom in residue:
        new_res.add(residue[keep_atom])
  
    chain = residue.get_parent()
    chain.detach_child(residue.get_id())
    chain.add(new_res)

  def get_orthogonal_vector(self, vect):
    '''Get an normalized othorgonal vector the the given vector.'''
    oth_vect = np.cross(vect, np.array([1, 0, 0]))
    if 0 == np.dot(oth_vect, oth_vect):
      oth_vect = np.cross(vect, np.array([0, 1, 0]))
    return oth_vect / np.linalg.norm(oth_vect)

  def straightify_loop(self, structure, loop):
    line_begin = structure[loop.model][loop.chain][loop.begin]['CA'].coord
    line_end = structure[loop.model][loop.chain][loop.end]['CA'].coord
    line_vect = line_end - line_begin
    seg_vect = line_vect / (loop.end - loop.begin)
    oth_vect = self.get_orthogonal_vector(line_vect)

    structure[loop.model][loop.chain][loop.begin]['C'].coord = line_begin \
        + 1.0/3 * seg_vect

    for seqpos in range(loop.begin + 1, loop.end):
      structure[loop.model][loop.chain][seqpos]['CA'].coord = line_begin \
            + (seqpos - loop.begin) * seg_vect
      structure[loop.model][loop.chain][seqpos]['C'].coord = line_begin \
            + (seqpos - loop.begin + 1.0/3 ) * seg_vect + 0.5 * oth_vect
      structure[loop.model][loop.chain][seqpos]['N'].coord = line_begin \
            + (seqpos - loop.begin - 1.0/3 ) * seg_vect - oth_vect
    
    structure[loop.model][loop.chain][loop.end]['N'].coord = line_end \
        - 1.0/3 * seg_vect


  def normalize_one_loop(self, structure, loop):
    loop_residues = [structure[loop.model][loop.chain][seqpos] for seqpos in range(loop.begin, loop.end + 1)]
    
    # Remove the side chains of residues within self.cutoff
    
    nearby_residues = get_residues_nearby(loop_residues, structure, self.cutoff) 
    
    for res in nearby_residues:
      self.trim_one_residue(res, ['CA', 'C', 'N', 'O', 'H'])

    # Only keep the mainchain atoms of the loop
    
    for res in loop_residues:
      self.trim_one_residue(res, ['CA', 'C', 'N']) 
    
    # Make the loop a straight line

    self.straightify_loop(structure, loop)

  def apply(self, info_dict):
    parser = PDB.PDBParser()
    io = PDB.PDBIO()

    for structure_dict in info_dict['candidate_list']:
      structure = parser.get_structure('', structure_dict['path'])
      
      for loop in structure_dict['candidate_loop_list']:
        
        self.normalize_one_loop(structure, loop)
        
      io.set_structure(structure)
      tmp_pdb = os.path.join(os.path.dirname(structure_dict['path']), structure_dict['name'] + '_trimed.pdb')
      io.save(tmp_pdb)
      
      self.update_pdb(tmp_pdb,structure_dict['path']) 
