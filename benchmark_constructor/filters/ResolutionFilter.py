import Bio.PDB as PDB

from .Filter import Filter


class ResolutionFilter(Filter):
  ''' ResolutionFilter filters structures by their resolution '''
  def __init__(self, threshold=1.5):
    self.threshold = threshold

  def apply(self, info_dict):
    parser = PDB.PDBParser()
  
    # Iterate through a copy of the list, because the list might be modified
    for d_pdb in info_dict['candidate_list'][:]:
      structure = parser.get_structure('', d_pdb['path'])
      if structure.header['resolution'] > self.threshold:
        self.remove_structure(info_dict, d_pdb)
