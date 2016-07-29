Rules for writing a filter
--------------------------
1. All filters should be derived from Filter.

2. A filter should has a :code:`apply(self, info_dict)` that do the filtering.

3. Filters may change the :code:`info_dict`. So make sure that there is no conflict
between the filters you use. Also because of this, the filters are NOT COMMUTATIVE.

4. Use the :code:`remove_structure(self, info_dict, structure_dict)` function defined in the base class to remove a candidate structure. 
