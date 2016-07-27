def is_heavy_atom_no_water(atom):
  '''Return true if an atom is a heavy atom and not belongs to a water molecule'''
  if atom.get_parent().get_resname() == 'HOH':
    return False
        
  return is_heavy_atom(atom)

  
def is_heavy_atom(atom):
  '''Return true if an atom is a heavy atom.'''   
  name = atom.get_id()
  if name[0] == 'H':
    return False
    
  if ord(name[0]) >= ord('0') and ord(name[0]) <= ord('9') and name[1] == 'H':
    return False

  return True


def Coarse_secondary_structure(ss):
  '''Convert fine grind secondary structures to coarse grind seconday structures'''
  helices = ['H', 'G', 'I']
  strands = ['B', 'E']
  if ss in helices: return 'helix'
  if ss in strands: return 'strand'
  return 'loop'


