import os
import shutil

class Filter:
  '''Base class for filters'''
  def __init__(self):
    pass

  def remove_structure(self, info_dict, structure_dict):
    '''Remove a structure from the candidate list'''
    shutil.rmtree(os.path.dirname(structure_dict['path']))
    info_dict['candidate_list'].remove(structure_dict)

  def apply(self, info_dict):
    '''This is a pure virtual function'''
    raise Exception('The apply(self, info_dict) function of class {0} is not implemented'.format(type(self).__name__))
