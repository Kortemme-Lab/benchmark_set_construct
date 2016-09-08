Benchmark set construct
=======================
This repository contains scripts that can help you create benchmark data
set for protein modeling or protein design. 

Dependencies
------------
python3

`docopt <http://docopt.org/>`_

`Biopython <http://biopython.org/>`_

`DSSP <http://swift.cmbi.ru.nl/gv/dssp/>`_

`MSMS <http://mgl.scripps.edu/people/sanner/html/msms_home.html>`_

`PyMol <https://www.pymol.org>`_

You can use the :code:`dependencies/install_dependencies.py` script to install Biopython and docopt.
It can also download DSSP for you. But you need to install DSSP, MSMS and PyMol yourself (make sure that dssp, msms
and pymol are in your PATH).

Get started
-----------
Before diving into how these scripts work, let's try an example first. Make
sure that the dependency packages and applications are installed. Then run::

  ./run_benchmark_constructor.py my_set job_scripts/multiple_loop.py -a inputs/kic/

This will take a couple of minutes to finish. Then you will find that a :code:`data/0_my_set/`
directory is created. Inside this directory is the benchmark set constructed by the
scripts.

How does it work?
-----------------
In general, constructing a benchmark dataset usually has three steps:

  1. Collect a set of candidate structures.
  
  2. Filter out structures that don't meet certain criteria.
  
  3. Write the structual information into specific file format.
  
The :code:`benchmark_constructor` module provides some :code:`structure_collectors`,
:code:`filters` and :code:`file_normalizers` to do the jobs listed above. You can
also write your own customized classes. After getting all the classes you need, you
need to assemble them into a python script (see :code:`job_scripts/multiple_loop.py`
as an example) and run the script with :code:`run_benchmark_constructor.py`. You can
run you job either in sequential or parallel. See :code:`benchmark_constructor/README.rst`
for writing new classes.
