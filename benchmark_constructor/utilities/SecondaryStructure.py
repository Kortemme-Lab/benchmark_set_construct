import Bio.PDB as PDB


class SecondaryStructure:
  '''This class represents a stretch of secondary structure of a protein.'''
  def __init__(self):
    pass

  def __repr__(self):
    s = '<{0}: begin {1}, end {2}, chain {3}, model {4}>'.format(self.type,
          self.begin, self.end, self.chain, self.model)
    return s

  def __lt__(self, s_structure2):
    if self.model < s_structure2.model:
      return True
    elif self.model == s_structure2.model:
      if self.chain < s_structure2.chain:
        return True
      elif self.chain == s_structure2.chain:
        if self.begin < s_structure2.begin:
          return True
        elif self.begin == s_structure2.begin:
          return self.end < s_structure2.end
        
    return False
  
  def connected(self, s_structure2, cutoff=1):
    '''Return true if the sequential distance between secondary structure1 and 
       secondary structure2 is littler than or equal to a cutoff.
    '''
    overlap = self.model == s_structure2.model \
              and self.chain == s_structure2.chain \
              and ((self.begin >= s_structure2.begin - cutoff and self.begin <= s_structure2.end + cutoff)
                   or (self.end >= s_structure2.begin - cutoff and self.end <= s_structure2.end + cutoff)
                   or (s_structure2.begin >= self.begin - cutoff and s_structure2.begin <= self.end + cutoff))
    return overlap

  def chop_up(self, length):
    '''Chop up the secondary structure into a list of secondary structures with length'''
    return [ type(self)(i, i + length - 1, self.chain, self.model) \
            for i in range(self.begin, self.end + 1) if i + length - 1 <= self.end ]
  
  def get_res_list(self, structure):
    '''Get the list of residues of the secondary structure.'''
    return [structure[self.model][self.chain][i] for i in range(self.begin, self.end+1)] 


def Coarse_secondary_structure(ss):
  '''Convert fine grind secondary structures to coarse grind seconday structures'''
  helices = ['H', 'G', 'I']
  #strands = ['B', 'E']
  strands = ['E'] # No more take isolated beta bridge as strands
  if ss in helices: return 'helix'
  if ss in strands: return 'strand'
  return 'loop'


def find_secondary_structures(pdb_file, required_ss_type, SSClass):
  '''Return a list of specific secondary structures.'''
  s_structure_list = []
  
  parser = PDB.PDBParser()
  structure = parser.get_structure('', pdb_file)
 
  for model_id, model in enumerate(structure):
    # Calculate the secondary structures of a model with DSSP

    dssp = PDB.DSSP(model, pdb_file)
    keys = list( dssp.keys() )
    if len(keys) == 0: return s_structure_list

    # Get all transition points of secondary structures. If a residue is neither helix or strand, it is deemed as a part of a s_structure.

    transition_points = [0]
    
    for i in range(1, len(keys)):
      res_info = dssp[keys[i]]
      res_info_prev = dssp[keys[i-1]]
      
      if keys[i][0] != keys[i-1][0] \
         or keys[i][1][1] != keys[i-1][1][1] + 1 \
         or Coarse_secondary_structure(res_info[2]) != Coarse_secondary_structure(res_info_prev[2]):
         transition_points.append(i)
    
    # Get required secondary structures
    
    for i, t in enumerate(transition_points):
      ss_type = Coarse_secondary_structure( dssp[keys[t]][2] )
      if ss_type != required_ss_type: continue

      chain = keys[t][0]
      start = keys[t][1][1]
      end = keys[transition_points[i+1] - 1][1][1] if i < len(transition_points)-1 else keys[-1][1][1] 

      s_structure_list.append(SSClass(start, end, chain=chain, model=model_id))

  # The best container for s_structures is ordered set which is not supported by official python package. So
  # use a list as container as a compromise.
  return s_structure_list
