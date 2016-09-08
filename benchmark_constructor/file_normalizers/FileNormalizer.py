import shutil


class FileNormalizer():
  '''Base class for file normalizers'''
  def __init__(self):
    pass


class UpdatePDBNormalizer(FileNormalizer):
  '''Base class for file normalizers that update the PDB file'''
  def __init__(self):
    pass

  def update_pdb(self, new_pdb_path, pdb_path):
    shutil.move(new_pdb_path, pdb_path)
