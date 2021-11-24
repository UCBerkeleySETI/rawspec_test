## Overview

Rawspec issue 39 is about an anomaly observed when switching between GPU devices.

## Required at the site
* The site must have at least 2 GPUs.
* The .raw file has sufficient data for 2 antennas.

## Preparation
* Edit ```rungen.sh```:
     - Adjust ```export PATH``` so that the rawspec executable for testing is first.
     - Adjust ```export LD_LIBRARY_PATH``` so that the rawspec library for testing is first.
     - Change ```STEM``` to indicate the rawspec file stem.
     - ```PARMS``` should need no changes.
     - Change the GPU device IDs (```testsession N```) as appropriate for the site.

## Execution
* Run  ```rungen.sh```.
* Run  ```rundiffs.sh```.

## Observe
* All the stdout from 3 ```diff``` executions should be nil.
* This was true for ant001 and ics.
* However, it was not true for ant000.
