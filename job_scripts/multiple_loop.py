#!/usr/bin/env python3
'''
Sequential script for creating a multiple loop dataset
'''

import sys

import benchmark_constructor as BC


if __name__ == '__main__':
  dataset_dir = sys.argv[1]
  input_dir = sys.argv[2]

  # Register structure collectors
  
  collector = BC.structure_collectors.CopyCollector(input_dir, dataset_dir)

  # Register filters

  filters = [ BC.filters.ResolutionFilter(2),
              BC.filters.LoopModelChainFilter(0, 'A'),
              BC.filters.LoopCrystalContactFilter(4, model=0, chain_list=['A'], pymol_bin='pymol'),
              BC.filters.LoopLengthFilter(9, 12),
              BC.filters.StructuredLoopFilter(12, 0, model=0),
              BC.filters.TerminalLoopFilter(5),
              BC.filters.MultipleLoopFilter(4, sequence_separation=5),
              ] 
  
  # Register normalizers
  
  normalizers = [ BC.file_normalizers.RosettaLoopNormalizer(),
                  BC.file_normalizers.FastaFileNormalizer(),
                  ] 
 
  # Apply everything
  
  BC.flow_control.sequential_apply(collector, filters, normalizers) 
