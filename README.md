# rawspec_test

The purpose of this repository is to support regression testing whenever a ```rawspec``` Pull Request is entertained.  In addition, it can be used by a developer on demand to augment unit-testing.

### Test Baseline Installation

The ```rawspec``` testing baseline resides at  ```/datax/scratch/rawspec_test_baseline/``` on node ```blpc0``` and consists of the following:
* .raw files provided by Matt Lebofsky
* 2 table files for each 0000.raw file as a result of running ```rawspec``` and ```turbo_seti``` in succession, representing baseline results that will be used for validating future ```rawspec``` runs. 

The intermediate *.fil file produced by ```rawspec``` and the intermediate *.h5, *.dat, and *.log files produced by ```turbo_seti``` have been discarded. 
 
The table files are of the following types:
* ```*.tbldat``` top_hit_id, drift_rate, snr,frequency, and total_num_hits values extracted from the corresponding ```turbo_seti``` .dat file.
* ```*.tblhdr``` Filterbank header fields with the number of integrations added.

Both table file types are implemented as CSV files.


In theory, the installation only needs to be done once (famous last words?).  Of course, more test .raw files can be incorporated in the future to expand the testing scope.  Precisely how to add to the existing .raw file set and generate the new test table files is TBD (but not difficult).

As of 2021-10-31, this step was completed with the following script execution:
```python3 installer.py  -g 3```. 

## Test Baseline Contents

The following files are in the testing baseline directory:

blc13_guppi_57991_49836_DIAG_FRB121102_0010.0000.raw
blc13_guppi_57991_49836_DIAG_FRB121102_0010.0001.raw
blc13_guppi_57991_49836_DIAG_FRB121102_0010.0002.raw
blc13_guppi_57991_49836_DIAG_FRB121102_0010.rawspec.0000.tbldat
blc13_guppi_57991_49836_DIAG_FRB121102_0010.rawspec.0000.tblhdr
blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008.0000.raw
blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008.0001.raw
blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008.0002.raw
blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008.rawspec.0000.tbldat
blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008.rawspec.0000.tblhdr


## Prerequisites to Testing

* Login to any data centre node.
* If this repository (rawspec_test) has not yet been installed, then
     - ```git clone https://github.com/UCBerkeleySETI/rawspec_test```.
* Do the following Python package updates in the order specified:
     - ```pip  install  -U  --user  blimpy```
     - ```pip  install  -U  --user  turbo_seti```

## Testing a New Pull Request

* Login to any data centre node.
* Go to $HOME/rawspec_test/exec 
*  Edit the ```xprep.sh``` script to supply the PR's URL and BRANCH values.
* ```bash xprep.sh```
* ```bash xtest.sh  <GPU_ID>```

## xprep.sh Overview :: Prepare PR Copy of Rawspec for Testing

* `set -e` so that if anything goes wrong, immediately exit.
* Fix the CUDA_PATH environment variable: ```export CUDA_PATH=/usr/local/cuda```.
* Validate URL and BRANCH.
* Go $HOME.
* If an old rawspec exists under $HOME, purge it.
* `git clone -branch <BRANCH> <URL>`
* `cd rawspec`
* `make`

## xtest.sh Overview :: Run Tests and Evaluate Results

* `set -e` so that if anything goes wrong, immediately exit.
* Fix the PATH environment variable: ```export PATH=$HOME/rawspec:$PATH```.
* Set the LD_LIBRARY_PATH environment variable: ```export LD_LIBRARY_PATH=$HOME/rawspec```.
* Go to $HOME/rawspec_test/exec
* Generate trial results: ```python3 runner.py -g <GPU ID>```.
* Compare trial results to that of the baseline: ```python3 reviewer.py```.

### runner.py

The ```runner.py``` script builds a testing trial directory at ```/datax/scratch/rawspec_testing_trial/```.  This will replace any old trial artifacts that might have been left over from a previous execution.  Then, it runs ```rawspec```, ```turbo_seti```, and the testing utility scripts (```dat2tbl.py``` and ```hdr2tbl.py```).

### reviewer.py

The ```reviewer.py``` script compares the corresponding table files from the baseline and trial directories.  Successful comparisons are logged as informational messages.  Discrepancies are logged as errors.  Any error found should be investigated as soon as possible.
