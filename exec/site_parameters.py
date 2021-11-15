"""
Package rawspec_testing
Site parameters.
"""

SOURCE_DIR_1 = "/mnt_blpd5/datax/FRB121102/BLP13/"

SOURCE_DIR_2 = "/mnt_blpd5/datax/FRB121102/BLP17/"

RAWSPEC_TESTING_DIR = "/mnt_blpd20/scratch/rawspec_testing/"

ATA_DIR = RAWSPEC_TESTING_DIR + "ata/" # Only used in the UC Berkeley data centre as a source of files to link.

SELECTED = [ # List of files to actually link into baseline and trial directories
    SOURCE_DIR_1 + "blc13_guppi_57991_49836_DIAG_FRB121102_0010",
    SOURCE_DIR_2 + "blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008",
    ]

RUN_TURBO_SETI = False
