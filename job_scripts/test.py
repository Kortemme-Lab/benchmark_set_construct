#!/usr/bin/env python3

import sys

import benchmark_constructor as BC


if __name__ == '__main__':
  dataset_dir = sys.argv[1]

  # Register structure collectors
  
  collector = BC.structure_collectors.CopyCollector('inputs/kic', dataset_dir)

  # Register filters

  filters = [ BC.filters.ResolutionFilter(1.5),
              BC.filters.LoopModelChainFilter(0, 'A'),
              BC.filters.LoopLengthFilter(12),
              BC.filters.LoopCrystalContactFilter(4, model=0, chain_list=['A'], pymol_bin='pymol')] 
  
  # Register normalizers
  
  normalizers = [ BC.file_normalizers.LoopFileNormalizer() ] 
 
  # Apply everything
  
  BC.flow_control.sequential_apply(collector, filters, normalizers) 
