import os
import subprocess

from Bio import PDB
from Bio.Data import SCOPData

from .FileNormalizer import FileNormalizer 

class FastaFileNormalizer(FileNormalizer):
  '''Create a FASTA file that has the sequence of the structure'''
  def __init__(self):
    pass

  def apply(self, info_dict):
    parser = PDB.PDBParser()

    for structure_dict in info_dict['candidate_list']:
      
      structure = parser.get_structure('', structure_dict['path'])

      fasta_path = os.path.join(os.path.dirname(structure_dict['path']),
                                 structure_dict['name'] + '.fasta')
     
      with open(fasta_path, 'w') as f:
        
        for chain in structure[0]:
          f.write('>{0}|{1}\n'.format(structure_dict['name'], chain.get_id()))
          
          for res in chain:
            f.write(SCOPData.protein_letters_3to1.get(res.get_resname(), ''))
          f.write('\n')
