import os
import subprocess

from .FileNormalizer import UpdatePDBNormalizer

class PackRotamerNormalizer(UpdatePDBNormalizer):
  '''Pack rotamers of the PDB file using Rosetta'''
  def __init__(self, rosetta_scripts_cmd, script_file_path, rosetta_database=None):
    self.rosetta_scripts_cmd = rosetta_scripts_cmd
    self.script_file_path = script_file_path
    self.rosetta_database = rosetta_database

  def apply(self, info_dict):
    
    for structure_dict in info_dict['candidate_list']:
      cmd = [self.rosetta_scripts_cmd,
             '-in:file:s', structure_dict['path'],
             '-in:ignore_unrecognized_res',
             '-out:prefix', os.path.dirname(structure_dict['path']) + '/',
             '-run:no_scorefile',
             '-detect_disulf', 'false', #To avoid Rosetta crash
             '-parser:protocol', self.script_file_path,]

      if self.rosetta_database:
        cmd += ['-in:path:database', self.rosetta_database]
      
      subprocess.check_call(cmd)

      new_pdb = os.path.join(os.path.dirname(structure_dict['path']),
                             structure_dict['name'] + '_0001.pdb')

      self.update_pdb(new_pdb, structure_dict['path'])
