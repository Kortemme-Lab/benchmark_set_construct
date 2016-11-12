import os
import subprocess

import Bio.PDB as PDB

from .FileNormalizer import FileNormalizer
from .FileNormalizer import UpdatePDBNormalizer
from .LoopFileNormalizer import LoopFileNormalizer
from .utilities.Loop import Loop

class RosettaFileNormalizer(FileNormalizer):
  ''' RosettaFileNormalizer is the base class for generating Rosetta input
      files. This is an abstract class.
  '''
  def __init__(self):
    pass

  def apply(self, info_dict):
    raise Exception('RosettaFileNormalizer is an abstract class!')

  def get_residue_map(self, pdb_path):
    ''' Get a map from residue indices to Rosetta indices. '''
    parser = PDB.PDBParser()
    structure = parser.get_structure('', pdb_path)

    res_map = {}

    for model in structure:
      model_id = model.get_id()

      for chain in model:
        chain_id = chain.get_id()

        res_id_list = [res.get_id()[1] for res in chain]

        for i, res_id in enumerate(res_id_list):
          res_map[(model_id, chain_id, res_id)] = i + 1
          
    return res_map
    
  def get_all_residue_map(self, info_dict):
    ''' Get residue maps for each structure in a info_dict. '''
    for structure_dict in info_dict['candidate_list']:
      if 'Rosetta_residue_map' not in structure_dict.keys():
        structure_dict['Rosetta_residue_map'] = self.get_residue_map(structure_dict['path'])
        
        
class RosettaLoopNormalizer(RosettaFileNormalizer, LoopFileNormalizer):
  '''RosettaLoopNormalizer creates loop files with Rosetta numbers. '''
  def __init__(self):
    pass

  def apply(self, info_dict):
    self.get_all_residue_map(info_dict)
    
    for structure_dict in info_dict['candidate_list']:
      d = os.path.dirname(structure_dict['path']) 
     
      if 'candidate_loop_list' in structure_dict.keys():
        rosetta_nl = structure_dict['name'] + '_rosetta.loop'
        rosetta_ns = structure_dict['name'] + '_select_rosetta_loop.pml'
        pdb_nl = structure_dict['name'] + '_pdb.loop'
        pdb_ns = structure_dict['name'] + '_select_pdb_loop.pml'
        
        # Create a new list of loops in Rosetta number

        rosetta_loop_list = []
        for loop in structure_dict['candidate_loop_list']:
          begin = structure_dict['Rosetta_residue_map'][(loop.model, loop.chain, loop.begin)]
          end = structure_dict['Rosetta_residue_map'][loop.model, loop.chain, loop.end]
          rosetta_loop_list.append(Loop(begin, end, loop.chain, loop.model))

        self.normalize_one_file(os.path.join(d, rosetta_nl), os.path.join(d, rosetta_ns), rosetta_loop_list)
        self.normalize_one_file(os.path.join(d, pdb_nl), os.path.join(d, pdb_ns), structure_dict['candidate_loop_list'])

      if 'adjacent_loop_pair_set' in structure_dict.keys():
        nlp = structure_dict['name'] + '_rosetta_adjacent_pairs.loop'

        # Create a new list of loop pairs in Rosetta number

        rosetta_loop_pair_list = []
        for lp in structure_dict['adjacent_loop_pair_set']:
          
          begin0 = structure_dict['Rosetta_residue_map'][(lp[0].model, lp[0].chain, lp[0].begin)]
          end0 = structure_dict['Rosetta_residue_map'][lp[0].model, lp[0].chain, lp[0].end]
          begin1 = structure_dict['Rosetta_residue_map'][(lp[1].model, lp[1].chain, lp[1].begin)]
          end1 = structure_dict['Rosetta_residue_map'][lp[1].model, lp[1].chain, lp[1].end]

          rosetta_loop_pair_list.append((Loop(begin0, end0, lp[0].chain, lp[0].model),
                                         Loop(begin1, end1, lp[1].chain, lp[1].model)))

        self.normalize_adjacent_loop_pairs(os.path.join(d, nlp), set(rosetta_loop_pair_list))


class RosettaCleanPDBNormalizer(RosettaFileNormalizer, UpdatePDBNormalizer):
  '''RosettaCleanPDBNormalizer create a new PDB file that is cleaned up for Rosetta.
     The clean_pdb.py script of Rosetta tools is required.
  '''
  def __init__(self, clean_script_path):
    self.clean_script_path = clean_script_path

  def apply(self, info_dict):
    print("WARNING: RosettaCleanPDBNormalizer will change the indices of the PDB file.",
      "This will results in indexing discrepancy between the native PDB file.")
    
    cwd = os.getcwd()
    
    for structure_dict in info_dict['candidate_list']:
      os.chdir(os.path.dirname(structure_dict['path']))
  
      # Clean the PDB file and rename it
  
      subprocess.check_call(['python2.7', self.clean_script_path,
                             structure_dict['name']+'.pdb', 'ignorechain'])
                   
      # Remove the FASTA file which is a by-product of clean_pdb.py
  
      os.remove(structure_dict['name'] + '_ignorechain.fasta')

      # Update the pdb file

      self.update_pdb(structure_dict['name'] + '_ignorechain.pdb', structure_dict['name'] + '.pdb')
      os.chdir(cwd)
