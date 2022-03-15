# rawspec_testing

The purpose of this repository is to support regression testing whenever a ```rawspec``` Pull Request (PR) is entertained.  In addition, a developer should use it as part of unit-testing to ensure that nothing was inadvertently broken.

## 1.0 Rawspec Testing Directory Tree Overview

The ```rawspec``` testing directory tree is rooted at  ```/mnt_blpd20/scratch/rawspec_testing/``` on data centre compute node ```blpc1```.  There are 2 subdirectories underneath:
* ```baseline``` - Expected results.  See discussion of ```xinstall.sh```.
* ```trial``` - Trial results from a candidate for updating the ```rawspec``` master branch at UCBerkeleySETI on github.  A PR is an example of such a candidate.  See discussion of ```xtest.sh``` 

The ```baseline``` subdirectory at the UCB data centre consists of the following:
* **Input** GBT .raw files provided by @mattlebofsky (Matt Lebofsky):
     - FRB .raw files, used to produce a single output .fil file.
     - Pulsar .raw files, used to produce 3 output .fil files, an exercise of output product multithreading.
* A single **input** ATA-supplied synthetic .raw file, used to produce:
     - 2 antenna output .fil files.
     - 1 incoherent sum (ics) output .fil file.
* The **intermediate** .fil files, produced by ```rawspec```.
* Two **output** table files for each .fil file, created by Python test utilities.
* One **output** table file produced after running ```rawspectest```, created by another Python test utility.

The table files are as follows:
* ```*.tblhdr``` Filterbank header fields, 1 row per field, plus 1 row for the number of integrations as an addition.
* ```*.tbldsel``` Selected Filterbank data matrix fields.  Currently, 15 values are recorded: 3 each at the 4 data corners plus 3 at the centre.
* ```rawspectest.tblnpols``` Output from a rawspectest session with ```nbits``` values of 4, 8, and 16.

All table file types are implemented as CSV files.

The ```trial``` subdirectory contains the same intermediate and output files.  Note that there are no .raw files in the trial subdirectory.

The following is a listing of the baseline subdirectory in the UCB Data Centre:
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

* Login to any data centre node.
* If this repository (rawspec_testing) has not yet been installed, then go $HOME and do the following:
     - ```git clone https://github.com/UCBerkeleySETI/rawspec_testing```.
* Install/reinstall blimpy: ```pip  install  -U  --user  blimpy```.

## 3.0 Testing Operations

### 3.1 Installing the Testing Baseline (caution!)

IMPORTANT: This procedure is unnecessary for PR testing and has the potential to be disruptive.  It should only be performed when there are changes to the site parameters or to the baseline .raw file data itself.

* Login to any data centre node.
* Go to $HOME/rawspec_testing/exec 
* Edit ```site_parameters.py``` as appropriate for the new/updated local site.
* ```bash xinstall.sh  <GPU_ID (0, 2, 3, or 3)>```

### 3.2 Testing a New Pull Request

* Login to any data centre node.
* Go to $HOME/rawspec_testing/exec 
* With nano, edit the ```xprep.sh``` script to supply the PR's main URL value and the specific BRANCH name value.  The URL string should end in “…./rawspec”.
* An alternative is to use the Visual Studio Code GUI to edit the ```xprep.sh``` script.
* Then, run ```bash xprep.sh``` to set up testing with the PR code base.
* Finally, run ```bash xtest.sh  <GPU_ID (0, 2, 3, or 3)>```
* Success should be announced on both the SIGPROC and FBH5 sections of testing.

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
