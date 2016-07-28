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
