#!/usr/bin/env python

__author__ = "Joshua Shorenstein"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Joshua Shorenstein"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Joshua Shorenstein"
__email__ = "jshorens@gmail.com"
__status__ = "Development"

from os import walk
from os.path import exists
from sys import argv


def get_mapping_filepaths(basefolder, level):
    """Combs basefolder to get all mapping files for given level
        MUST USE FOLLOWING FOLDER STRUCTURE:
        basefolder/STUDY/summarize_taxa/mapping_file_L#.txt

        basefolder: folderpath containing all studies
        level: level of summarize_taxa data to return (integer)
    """
    #add trailing slash to basefolder if neccessary
    if basefolder[:-1] != "/":
        basefolder += "/"

    level = "L" + str(level)

    filepaths = []
    #loop over each study in the basefolder
    for study in walk(basefolder).next()[1]:
        fp1 = ''.join([basefolder, study, "/summarize_taxa/mapping_file_", 
            level, ".txt"])
        fp2 = ''.join([basefolder, study, "/summarize_taxa_feces/mapping_file_",
            level, ".txt"])
        #check that the mapping filepath exists
        if exists(fp1):
            filepaths.append(fp1)
        elif exists(fp2):
            filepaths.append(fp2)
        else:
            print "NO MAPPING FILE FOR " + basefolder + study
    return filepaths


if __name__ == "__main__":
    print ','.join(get_mapping_filepaths(argv[1], argv[2]))