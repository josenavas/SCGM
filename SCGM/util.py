#!/usr/bin/env python

__author__ = "Joshua Shorenstein"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Joshua Shorenstein", "Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Joshua Shorenstein"
__email__ = "jshorens@gmail.com"
__status__ = "Development"

from os.path import exists, join

# from os import walk
# from os.path import exists, join

# def get_mapping_filepaths(basefolder, level):
#     """Combs basefolder to get all mapping files for given level
#         MUST USE ONE OF THE FOLLOWING FOLDER STRUCTURE:
#             basefolder/STUDY/summarize_taxa/mapping_file_L#.txt
#         or:
#             basefolder/STUDY/summarize_taxa_feces/mapping_file_L#.txt

#         basefolder: folderpath containing all studies
#         level: level of summarize_taxa data to return (integer)

#         Returns:
#         a list containing the paths to the mapping files
#     """
#     filepaths = []
#     #loop over each study in the basefolder
#     for study in walk(basefolder).next()[1]:
#         fp1 = join(basefolder, study, "/summarize_taxa/mapping_file_L" + 
#             str(level) + ".txt")
#         fp2 = join(basefolder, study, "/summarize_taxa_feces/mapping_file_L" + 
#             str(level) + ".txt")
#         #check that the mapping filepath exists
#         if exists(fp1):
#             filepaths.append(fp1)
#         elif exists(fp2):
#             filepaths.append(fp2)
#         else:
#             print "NO MAPPING FILE FOR " + basefolder + study
#     return filepaths

def check_exist_filepaths(base_dir, mapping_fps):
    """Check that all the mapping files in mapping_fps exist

    Inputs:
        base_dir: the common directory path where all the mapping_fps are 
            relative to
        mapping_fps: a list with the relative filepaths from base_dir to the
            mapping files

    If any of the filepaths does not exists, raises a ValueError
    """
    for fp in mapping_fps:
        fullpath = join(base_dir, fp)
        if not exists(fullpath):
            raise ValueError, "The mapping file %s does not exists" % fullpath