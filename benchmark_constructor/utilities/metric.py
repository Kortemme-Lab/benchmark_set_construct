import Bio.PDB as PDB

from .Chemistry import is_heavy_atom

def residue_pair_distance(res1, res2, heavy_only=True):
  '''Calculate the distance between a pair of atoms. The distance is 
     defined as the shortest distance between pair of atoms in the two
     residues respectively.
  '''
  distance = float('+inf')
  for a1 in res1:
    if heavy_only and not is_heavy_atom(a1):
      continue
    
    for a2 in res2:
      if heavy_only and not is_heavy_atom(a2):
        continue
      
      d = a1 - a2
      if d < distance:
        distance = d

  return distance


def residue_group_distance(res_list1, res_list2, heavy_only=True):
  '''Calculate the distance between two groups of residues. The distance is
     defined as the shortest distance between pair of residues in the two
     groups respectively.
  '''
  distance = float('+inf')
  
  for r1 in res_list1:
    for r2 in res_list2:
      d = residue_pair_distance(r1, r2, heavy_only)
      if d < distance:
        distance = d

  return distance


def get_residues_nearby(res_list, structure, cutoff):
  '''Get a list of residues whose CA-CA distance from the given residue list is within
     the cutoff.
  '''
  center_atoms = [atom for res in res_list for atom in res if atom.name == 'CA']
  atom_list = [atom for atom in structure.get_atoms() 
               if (atom.name == 'CA' and not atom in center_atoms)]

  ns = PDB.NeighborSearch(atom_list)
  nearby_residues = {atom.get_parent() for center_atom in center_atoms
                       for atom in ns.search(center_atom.coord, cutoff, 'A')} 

  return list(nearby_residues)


def get_residues_depth(res_list, model, pdb_file):
  '''Get the average depth of a list of residues. The msms program is required.
  '''
  rd = PDB.ResidueDepth(model, pdb_file)
  
  depth_list = []
  for res in res_list:
    res_id = (res.get_parent().get_id(), res.get_id())
    depth_list.append(rd[res_id][0] if res_id in rd else 0)

  return sum(depth_list)/len(res_list)
