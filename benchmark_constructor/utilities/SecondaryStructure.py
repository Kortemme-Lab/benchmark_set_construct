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


