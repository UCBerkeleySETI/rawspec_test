# rawspec_testing

The purpose of this repository is to support regression testing whenever a ```rawspec``` Pull Request is entertained.  In addition, it can be used by a developer on demand to augment unit-testing.

## 1.0 Testing Baseline Overview

The ```rawspec``` testing baseline resides at  ```/mnt_blpd20/scratch/rawspec_testing/baseline/``` and consists of the following:
* GBT .raw files provided by @mattlebofsky (Matt Lebofsky)
* ATA-supplied test .raw file.
* 2 table files for each output .fil file as a result of running ```rawspec```.
* 1 table file produced by a rawspectest session.

The table files are as follows:
* ```*.tblhdr``` Filterbank header fields with a row for the number of integrations added.
* ```*.tbldsel``` Selected Filterbank data fields.
* ```rawspectest.tblnpols``` Output from a rawspectest session with ```nbits``` values of 4, 8, and 16.

All table file types are implemented as CSV files.

The following is a listing of the testing baseline directory:
```
ATA_guppi_59229_47368_006379_40blocks.0000.raw
ATA_guppi_59229_47368_006379_40blocks-ant000.rawspec.0000.fil
ATA_guppi_59229_47368_006379_40blocks-ant000.rawspec.0000.tbldsel
ATA_guppi_59229_47368_006379_40blocks-ant000.rawspec.0000.tblhdr
ATA_guppi_59229_47368_006379_40blocks-ant001.rawspec.0000.fil
ATA_guppi_59229_47368_006379_40blocks-ant001.rawspec.0000.tbldsel
ATA_guppi_59229_47368_006379_40blocks-ant001.rawspec.0000.tblhdr
ATA_guppi_59229_47368_006379_40blocks-ics.rawspec.0000.fil
ATA_guppi_59229_47368_006379_40blocks-ics.rawspec.0000.tbldsel
ATA_guppi_59229_47368_006379_40blocks-ics.rawspec.0000.tblhdr
blc13_guppi_57991_49836_DIAG_FRB121102_0010.0000.raw
blc13_guppi_57991_49836_DIAG_FRB121102_0010.0001.raw
blc13_guppi_57991_49836_DIAG_FRB121102_0010.0002.raw
blc13_guppi_57991_49836_DIAG_FRB121102_0010.rawspec.0000.fil
blc13_guppi_57991_49836_DIAG_FRB121102_0010.rawspec.0000.tbldsel
blc13_guppi_57991_49836_DIAG_FRB121102_0010.rawspec.0000.tblhdr
blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008.0000.raw
blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008.0001.raw
blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008.0002.raw
blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008.rawspec.0000.fil
blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008.rawspec.0000.tbldsel
blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008.rawspec.0000.tblhdr
blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008.rawspec.0001.fil
blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008.rawspec.0001.tbldsel
blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008.rawspec.0001.tblhdr
blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008.rawspec.0002.fil
blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008.rawspec.0002.tbldsel
blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008.rawspec.0002.tblhdr
rawspectest.tblnpols

```

## 1.1 Site Parameters

The module ```exec/site_parameters.py``` contains all of the site parameters.  Editing them necessitates an installation afterwards (see the section below entitled "Installing the Testing Baseline").

## 2.0 Prerequisites to All Activity

Before doing anything else related to rawspec_testing, follow this procedure.

* Login to data centre node blpc1.
* If this repository (rawspec_testing) has not yet been installed, then go $HOME and do the following:
     - ```git clone https://github.com/UCBerkeleySETI/rawspec_testing```.
* Install/reinstall blimpy: ```pip  install  -U  --user  blimpy```.

## 3.0 Testing Operations

### 3.1 Installing the Testing Baseline (caution!)

IMPORTANT: This procedure is unnecessary for PR testing and has the potential to be disruptive.  It should only be performed when there are changes to the site parameters or to the baseline .raw file data itself.

* Login to data centre node blpc1.
* Go to $HOME/rawspec_testing/exec 
* If needed, edit ```site_parameters.py``` as mentioned above.
* ```bash xinstall.sh  <GPU_ID (0, 2, 3, or 3)>```

### 3.2 Testing a New Pull Request

* Login to data centre node blpc1.
* Go to $HOME/rawspec_testing/exec 
* Edit the ```xprep.sh``` script to supply the PR's URL value and the specific BRANCH name value.  The URL string should end in “…./rawspec”.
* An alternative is to use JupyterLab or Visual Studio Code to edit the ```xprep.sh``` script.
* Then, run ```bash xprep.sh``` to set up testing with the PR code base.
* Finally, run ```bash xtest.sh  <GPU_ID (0, 2, 3, or 3)>```

## 4.0 Bash Script Design Overviews

### 4.1 xinstall.sh Overview :: Driver for the installer.py Python Script

* Fix the PATH environment variable: ```export PATH=$HOME/rawspec:$PATH```.
* Set the LD_LIBRARY_PATH environment variable: ```export LD_LIBRARY_PATH=$HOME/rawspec```.
* If an old rawspec exists under $HOME, purge it.
* `git clone -branch master https://github.com/UCBerkeleySETI/rawspec`
* `cd rawspec`
* `make`
* `python3 installer.py -g   <GPU_ID (0, 2, 3, or 3)>`

### 4.2 xprep.sh Overview :: Prepare PR Copy of Rawspec for Testing

* Validate URL and BRANCH.
* Go $HOME.
* If an old rawspec exists under $HOME, purge it.
* `git clone -b <BRANCH> <URL>`
* `cd rawspec`
* `make`

### 4.3 xtest.sh Overview :: Run Tests and Evaluate Results

* Fix the PATH environment variable: ```export PATH=$HOME/rawspec:$PATH```.
* Set the LD_LIBRARY_PATH environment variable: ```export LD_LIBRARY_PATH=$HOME/rawspec```.
* Go to $HOME/rawspec_testing/exec
* Generate trial results: ```python3 runner.py -g <GPU_ID (0, 2, 3, or 3)>```.
* Compare trial results to that of the baseline: ```python3 reviewer.py```.

## 5.0 Python Script Design Overviews

### 5.1 installer.py

* Print out system information and prompt the operator whether or not to continue (yes/no).
* Assume continuing.  All file creation will take place in the baseline directory.
* Run rawspec on all the file stems.
* For each Filterbank file produced by rawspec, 
     - Run hdr2tbl.main producing a .tblhdr file.
     - Run dsel2tbl.main producing a .tbldsel file.
* Run rawspectest for 4-, 8-, and 16-bits per second, producing combined table rawspectest.tblnpols.

### 5.2 runner.py

* Print out system information.
* All file creation will take place in the trial directory.
* Run rawspec on all the file stems in the baseline directory.
* For each Filterbank file produced by rawspec, 
     - Run hdr2tbl.main producing a .tblhdr file.
     - Run dsel2tbl.main producing a .tbldsel file.
* Run rawspectest for 4-, 8-, and 16-bits per second, producing combined table rawspectest.tblnpols.

### 5.3 reviewer.py

* Compare the corresponding table files from the baseline and trial directories.
* Discrepancies are logged as errors.  Any error found should be investigated as soon as possible.
