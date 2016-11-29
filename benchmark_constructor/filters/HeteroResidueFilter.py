import Bio.PDB as PDB

from .Filter import Filter


class HeteroResidueFilter(Filter):
  '''Remove structures that have hetero residues.
  '''
  def __init__(self):
    pass

  def structure_has_hetres(self, structure):
    for model in structure:
      for chain in model:
        for res in chain:
          if res.get_id()[0].startswith('H_'):
            print(res.get_id())
            return True
    return False
      
  def apply(self, info_dict):
    parser = PDB.PDBParser()

    # Iterate through a copy of the list, because the list might be modified
    for structure_dict in info_dict['candidate_list'][:]:
      structure = parser.get_structure('', structure_dict['path'])
      
      if self.structure_has_hetres(structure):
        self.remove_structure(info_dict, structure_dict)

