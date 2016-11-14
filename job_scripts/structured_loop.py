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

  filters = [ BC.filters.ResolutionFilter(2.0),
              BC.filters.LoopModelChainFilter(0, 'A'),
              BC.filters.LoopLengthFilter(5, 11),
              BC.filters.StructuredLoopFilter(16, 5, model=0),
              BC.filters.LoopCrystalContactFilter(4, model=0, chain_list=['A'], pymol_bin='pymol'),
              BC.filters.TerminalLoopFilter(5),
							BC.filters.LoopDepthFilter(1),
              ] 
  
  # Register normalizers
  
  normalizers = [ BC.file_normalizers.RosettaLoopNormalizer(),
                  BC.file_normalizers.LoopFileNormalizer(),
                 
                  BC.file_normalizers.MakeNativeCopyNormalizer(),
                  #BC.file_normalizers.PackRotamerNormalizer('/kortemmelab/home/xingjiepan/Softwares/Rosetta/main/source/bin/rosetta_scripts.linuxgccrelease',
                  #  'job_scripts/rosetta_repack.xml', 
                  #  '/kortemmelab/home/xingjiepan/Softwares/Rosetta/main/database'), 
                  BC.file_normalizers.LoopTrimNormalizer(10),
                  BC.file_normalizers.PymolCleanPDBNormalizer(),
                  ] 
 
  # Apply everything
  
  BC.flow_control.sequential_apply(collector, filters, normalizers) 
