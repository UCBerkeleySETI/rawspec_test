# rawspec_testing

The purpose of this repository is to support regression testing whenever a ```rawspec``` Pull Request is entertained.  In addition, it can be used by a developer on demand to augment unit-testing.

## 1.0 Testing Baseline Overview

The ```rawspec``` testing baseline resides at  ```/mnt_blpd20/scratch/rawspec_testing_baseline/``` and consists of the following:
* .raw files provided by Matt Lebofsky
* 2 table files for each 0000.raw file as a result of running ```rawspec``` and ```turbo_seti``` in succession. 
* 1 table file produced in a rawspectest session.

The intermediate *.fil file produced by ```rawspec``` and the intermediate *.h5, *.dat, and *.log files produced by ```turbo_seti``` have been discarded. 
 
The table files are as follows:
* ```*.tbldat``` top_hit_id, drift_rate, snr,frequency, and total_num_hits values extracted from the corresponding ```turbo_seti``` .dat file.
* ```*.tblhdr``` Filterbank header fields with the number of integrations added.
* ```rawspectest.tblnpols``` Output from a rawspectest session with ```nbits``` values of 8 and 16

All table file types are implemented as CSV files.

The following is a listing of the testing baseline directory (excluding the trial directory):
```
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
rawspectest.tblnpols
```
## 2.0 Prerequisites to All Activity

Before doing anything else related to rawspec_testing, follow this procedure.

* Login to any data centre node.
* If this repository (rawspec_testing) has not yet been installed, then
     - ```git clone https://github.com/UCBerkeleySETI/rawspec_testing```.
* Do the following Python package updates in the order specified:
     - ```pip  install  -U  --user  blimpy```
     - ```pip  install  -U  --user  turbo_seti```

## 3.0 Testing Operations

### 3.1 Installing the Testing Baseline (caution!)

IMPORTANT: This procedure is generally unnecessary for PR testing and has the potential to be disruptive.  It should only be performed when there are changes to the test data itself.  Still, consider simpler methods before using this procedure.

* Login to any data centre node.
* Go to $HOME/rawspec_testing/exec 
* ```bash xinstall.sh```

### 3.2 Testing a New Pull Request

* Login to any data centre node.
* Go to $HOME/rawspec_testing/exec 
*  Edit the ```xprep.sh``` script to supply the PR's URL and BRANCH values.
* ```bash xprep.sh```
* ```bash xtest.sh  <GPU_ID>```

## 4.0 Bash Script Overviews

### 4.1 xinstall.sh Overview :: Driver for the installer.py Python Script

* Fix the PATH environment variable: ```export PATH=$HOME/rawspec:$PATH```.
* Set the LD_LIBRARY_PATH environment variable: ```export LD_LIBRARY_PATH=$HOME/rawspec```.
* If an old rawspec exists under $HOME, purge it.
* `git clone -branch master https://github.com/UCBerkeleySETI/rawspec`
* `cd rawspec`
* `make`
* `python3 installer.py -g 3`

### 4.2 xprep.sh Overview :: Prepare PR Copy of Rawspec for Testing

* Validate URL and BRANCH.
* Go $HOME.
* If an old rawspec exists under $HOME, purge it.
* `git clone -branch <BRANCH> <URL>`
* `cd rawspec`
* `make`

### 4.3 xtest.sh Overview :: Run Tests and Evaluate Results

* Fix the PATH environment variable: ```export PATH=$HOME/rawspec:$PATH```.
* Set the LD_LIBRARY_PATH environment variable: ```export LD_LIBRARY_PATH=$HOME/rawspec```.
* Go to $HOME/rawspec_testing/exec
* Generate trial results: ```python3 runner.py -g <GPU ID>```.
* Compare trial results to that of the baseline: ```python3 reviewer.py```.

## 5.0 Python Script Overviews

### 5.1 installer.py

* Print out system information and prompt the operator whether or not to continue (yes/no).
* Assume continuing.  Purge everything under the existing baseline directory.
* Create the rawspectest baseline table.
* Copy over selected baseline .raw files from sources provided by Matt Lebofsky.
* Run rawspec on all the file stems.
* For each .fil file produced, run turboSETI.
* For each .h5 file either produced by rawspec directly or indirectly by turboSETI, run hdr2tbl.main producing a .tblhdr file.
* For each .dat file produced by turboSETI, run dat2tbl.main producing a .tbldat file.
* ```rm *.dat *.fil *.h5 *.log```.

### 5.2 runner.py

The ```runner.py``` script builds a testing trial directory at ```/mnt_blpd20/scratch/rawspec_testing_baseline/rawspec_testing_trial```.  This will replace any old trial artifacts that might have been left over from a previous execution.  Then, it runs ```rawspectest```, ```rawspec```, ```turbo_seti```, and the testing utility scripts (```npols2tbl.py```, ```dat2tbl.py```, and ```hdr2tbl.py```).  There are a lot of similarities between ```runner.py``` and ```installer.py```.

### 5.3 reviewer.py

The ```reviewer.py``` script compares the corresponding table files from the baseline and trial directories.  Successful comparisons are logged as informational messages.  Discrepancies are logged as errors.  Any error found should be investigated as soon as possible.
