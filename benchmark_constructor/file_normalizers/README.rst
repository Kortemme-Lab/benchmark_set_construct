Rules for writing a file normalizer
-----------------------------------
1. All file normalizers should be derived from FileNormalizer.

2. A file normalizer should have an :code:`apply(self, info_dict)` function that do the normalization.
