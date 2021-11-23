"""
Package rawspec_testing
Site parameters.

The following definitions reflect the UC Berkeley data centre compute nodes.
"""

TESTING_NODE = "blpc1"

# The root of all rawspec_testing artifacts.
RAWSPEC_TESTING_DIR = "/datax/scratch/rawspec_testing/"

# List of files to actually link into baseline and trial directories
SELECTED = [ 
    "blc13_guppi_57991_49836_DIAG_FRB121102_0010",
    "blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008",
    "ATA_guppi_59229_47368_006379_40blocks",
    ]

# The rawspec command-line options that are paired to the corresponding entry in SELECTED.
# SELECTED and RAWSPEC_OPTS are 1-to-1.
RAWSPEC_OPTS = [
    "-f 1048576  -t 51",
    "-f 1048576,8,1024 -t 51,128,3072",
    "-f 8192 -t 2 -S -i '1.0'",
    ]

# Baseline directory for measuring trial results to.
BASELINE_DIR = RAWSPEC_TESTING_DIR + "baseline/"

# The trial directory.
TRIAL_DIR = RAWSPEC_TESTING_DIR + "trial/"

# The table name for storing rawspectest results.
RAWSPECTEST_TBL = "rawspectest.tblnpols"

# Not using turbo_seti.
RUN_TURBO_SETI = False
