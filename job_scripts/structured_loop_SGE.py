#$ -S /netapp/home/xingjiepan/.local/bin/python3

'''
Sequential script for creating a multiple loop dataset
Run on SGE.
'''

import os
import sys
import sys; sys.path.append(os.getcwd())

import benchmark_constructor as BC


if __name__ == '__main__':
  BC.job_distributors.SGEJobDistributor.set_qb3cluster_environment()

  num_jobs = int(sys.argv[1])
  dataset_dir = sys.argv[2]
  input_dir = sys.argv[3]
  job_id = int(os.environ['SGE_TASK_ID'])

  # Register structure collectors
  
  collector = BC.structure_collectors.CopyCollector(input_dir, dataset_dir, num_jobs, job_id)

  # Register filters

  filters = [ BC.filters.ResolutionFilter(2.0),
              BC.filters.LoopModelChainFilter(0, 'A'),
              BC.filters.LoopLengthFilter(5, 7),
              BC.filters.StructuredLoopFilter(12, 5, model=0),
              BC.filters.LoopCrystalContactFilter(4, model=0, chain_list=['A'], pymol_bin='pymol'),
              BC.filters.TerminalLoopFilter(5),
							BC.filters.LoopDepthFilter(1),
              ] 
  
  # Register normalizers
  
  normalizers = [ BC.file_normalizers.RosettaLoopNormalizer(),
                 
                  BC.file_normalizers.MakeNativeCopyNormalizer(),
                  BC.file_normalizers.PackRotamerNormalizer('/netapp/home/xingjiepan/Rosetta/main/source/bin/rosetta_scripts.linuxgccrelease',
                    'job_scripts/rosetta_repack.xml', 
                    '/netapp/home/xingjiepan/Rosetta/main/database'), 
                  BC.file_normalizers.LoopTrimNormalizer(10),
                  ] 
 
  # Apply everything
  
  BC.flow_control.sequential_apply(collector, filters, normalizers) 
