"""
Package rawspec_testing
Site parameters.

The following definitions reflect the UC Berkeley data centre compute nodes.
"""

# The root of all rawspec_testing artifacts.
RAWSPEC_TESTING_DIR = "/mnt_blpd20/scratch/rawspec_testing/"

# Sources of .raw files to link.
SOURCE_DIR_1 = "/mnt_blpd5/datax/FRB121102/BLP13/"
SOURCE_DIR_2 = "/mnt_blpd5/datax/FRB121102/BLP17/"

# The following directory is only used in the UC Berkeley data centre as a source of files to link.
FROM_ATA_DIR = RAWSPEC_TESTING_DIR + "ata/" 

# List of files to actually link into baseline and trial directories
SELECTED = [ 
    SOURCE_DIR_1 + "blc13_guppi_57991_49836_DIAG_FRB121102_0010",
    SOURCE_DIR_2 + "blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008",
    FROM_ATA_DIR + "ATA_guppi_59229_47368_006379_40blocks",
    ]

# The rawspec command-line options that are paired to the corresponding entry in SELECTED.
# SELECTED and RAWSPEC_OPTS are 1-to-1.
RAWSPEC_OPTS = [
    "-f 1048576  -t 51",
    "-f 1048576  -t 51",
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
