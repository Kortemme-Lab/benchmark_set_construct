Benchmark constructor
=====================
This module provides a set of tools for protein benchmark set construction.

Data structure
--------------
The data structure used to pass information between :code:`structure_collectors`,
:code:`filters` and :code:`file_normalizers` has the following format::

  info_dict: {
    'candidate_list': [
      {
        'name':name1,
        'path':path1,
          ...other properties of structure1
      },
      {
        'name':name2,
        'path':path2,
          ...other properties of structure2
      },
      ...
    ]
    ...other properties of the whole data set
  }
