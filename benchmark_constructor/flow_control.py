'''This file contains functions that controls the way that
   structure_collectors, filters and file_normalizers are
   applied.
'''

def sequential_apply(structure_collector, filters, file_normalizers):
  '''Apply structure_collector, filters and file_normalizers sequentially.'''
  # Collect candidate structures
    
  info_dict = {'candidate_list':structure_collector.apply()}
        
  # Filter candidate structures
            
  for f in filters:
    f.apply(info_dict)
                        
  #  Normalize structures that passed filters
                            
  for n in file_normalizers:
    n.apply(info_dict)
