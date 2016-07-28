'''Functions for managing the storage of datasets'''

import os

def create_new_data_set(name, data_dir='data'):
  # Create the directory to save all data
  
  if not os.path.exists(data_dir): os.makedirs(data_dir)

  # Create a new data set directory with the name 'id_name'

  data_set_name = '_'.join( [str(get_new_data_set_id()), name] )
  data_set_path = os.path.join(data_dir, data_set_name)
  os.makedirs( data_set_path )

  return data_set_path


def get_new_data_set_id(data_dir='data'):
  current_ids = [ int(i.split('_')[0]) for i in os.listdir(data_dir) ]
  return 0 if len(current_ids) == 0 else 1 + max(current_ids)  
