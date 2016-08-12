#!/usr/bin/env python3

'''
Run jobs to create a dataset for benchmarking. Before launching this 
wrapper script. you should write your costumized script that consists 
of a structure_collector, a list of filters and a list of file_normalizers.
Then run your scripts with this wrapper.

Usage:
  run_benchmark_set_construct <name> <job-script> [options]

Arguments:
  <name>
    Name of the benchmark set.

  <job-script>
    Job script for the benchmark set construction.

Options:
  --job-distributor=<JD>, -d=<JD>  [default: sequential]
    Job distributor that runs the jobs.

  --job-script-arguments=<JA>, -a=<JA>  [default: ]
    Arguments passed to the job script. The job script will run
    as:
      job-script data-set-path job-script-arguments

  --num-jobs=<NJ>, -n=<NJ>
    Number of jobs for parallel run.
'''


import docopt

import benchmark_constructor as BC


if __name__ == '__main__':

  arguments = docopt.docopt(__doc__)

  # Convert job-script arguements into a list
  
  job_script_arguments = arguments['--job-script-arguments'].split()
  
  # Initialize the job distributor and run the job
  
  job_distributor = None

  if arguments['--job-distributor'] == 'sequential':
    job_distributor = BC.job_distributors.SequentialJobDistributor(arguments['<name>'],
                      arguments['<job-script>'], job_script_arguments)
    
    job_distributor.run()

  elif arguments['--job-distributor'] == 'SGE':
    job_distributor = BC.job_distributors.SGEJobDistributor(arguments['<name>'],
                      arguments['<job-script>'], job_script_arguments)

    num_jobs = arguments['--num-jobs'] if arguments['--num-jobs'] else 1
 
    job_distributor.run(num_jobs)

  else:
    raise IOError('Unknown job distributor: {0}'.format(arguments['--job-distributor']))


