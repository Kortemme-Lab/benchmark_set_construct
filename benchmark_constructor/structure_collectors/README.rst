Rules for writing a new structure collector
-------------------------------------------
1. All structure collectors should be derived from StructureCollector.

2. A structure collector should have an :code:`apply(self)` function that do the collecting job and return a candidate list with this format::

    [
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
