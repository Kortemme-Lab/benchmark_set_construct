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

`PyMol <https://www.pymol.org>`_

You can use the :code:`dependencies/install_dependencies.py` script to install Biopython and docopt. But you need to install DSSP and PyMol yourself.
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

