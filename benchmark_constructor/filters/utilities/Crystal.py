import os
import subprocess

import Bio.PDB as PDB

from .Chemistry import is_heavy_atom_no_water 


def create_crystal_packing_file(pdb_file, cutoff, pymol_bin='pymol', refresh=False):
  '''Create pdb files that contain crystal images within a cutoff from the 
     structure in the given pdb file. Return the list of PDB files created.
     PyMol is required.
  '''
  dir_name = os.path.dirname(pdb_file)
  pdb_name = os.path.basename(pdb_file).split('.')[0]
  new_pdb_path = os.path.join(dir_name, pdb_name+'_crystal_pack')
   
  if os.path.exists(new_pdb_path):
    if not refresh:
      return [os.path.join(new_pdb_path, f) for f in os.listdir(new_pdb_path)]
  else:
    os.makedirs(new_pdb_path)
  
  # Create a pymol script for asymmetric units generation

  pymol_script_name = os.path.join(dir_name, pdb_name+'_crystal_pack', pdb_name+'_crystal_pack.pml')

  pymol_script = '\n'.join(['from pymol import cmd',
                            'load {0}, native'.format(pdb_file),
                            'symexp X_, native, all, {0}'.format(cutoff),
                            'sym_objs = cmd.get_object_list(\'(X_*)\')',
                            'for obj in sym_objs: cmd.save(\'{0}\' + \'/\' + obj + \'.pdb\', obj)'.format(new_pdb_path)])

  with open(pymol_script_name, 'w') as ps:
    ps.write(pymol_script)

  # Run PyMol to create a new pdb file with asymmetric units

  subprocess.check_call([pymol_bin, '-c', pymol_script_name])
  
  return [os.path.join(new_pdb_path, f) for f in os.listdir(new_pdb_path)]


def get_crystal_contact_residues(pdb_file, cutoff, model=0, chain_list=['A'], pymol_bin='pymol', refresh=False):
  '''Get a set of residues on the structures have close contacts (within a cutoff)
     to the asymmetric units.
  '''
  # Create asymmetric units
  
  asym_list = create_crystal_packing_file(pdb_file, cutoff, pymol_bin, refresh)

  # Read the native structure and asymmetric units
  
  parser = PDB.PDBParser()
  native_structure = parser.get_structure(pdb_file, pdb_file)
  asym_structure_list = [parser.get_structure(s, s) for s in asym_list]
  
  # Get all non-water heavy atoms
  
  atm_list = [a for a in native_structure.get_atoms() if is_heavy_atom_no_water(a)]
  for asym_structure in asym_structure_list:
    atm_list += [a for a in asym_structure.get_atoms() if is_heavy_atom_no_water(a)]

  # Calculate atom pairs whose distance is within the cutoff
  
  ns = PDB.NeighborSearch(atm_list)
  atm_pair_list = ns.search_all(cutoff, level='A')

  # Get the set to return

  res_set = set()
  
  for ap in atm_pair_list:
    full_id0 = ap[0].get_full_id()
    full_id1 = ap[1].get_full_id()
    
    if full_id0[0] == pdb_file and full_id0[1] == model and full_id0[2] in chain_list \
       and full_id1[0] != pdb_file and full_id1[1] == model:
      res_id = ap[0].get_parent().get_id()
      if ' ' == res_id[0]: # Not hetero-atom
        res_set.add( (full_id0[2], res_id[1]) )
    
    elif full_id1[0] == pdb_file and full_id1[1] == model and full_id1[2] in chain_list \
       and full_id0[0] != pdb_file and full_id0[1] == model:
      res_id = ap[1].get_parent().get_id()
      if ' ' == res_id[0]: # Not hetero-atom
        res_set.add( (full_id0[2], res_id[1]) )
     
  return res_set


