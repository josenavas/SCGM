#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Jose Antonio Navas Molina", "Joshua Shorenstein", "Elizabeth Lor"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from SCGM.profile import make_profile_from_mapping, normalize_profiles, compare_profiles


def get_profiles_list(map_files, categories=None):
    """Creates a list of profiles for all map files, split by categories

    map_files: list of filepaths to mapping files
    categories: list of categories, one per map_file, same order as map_files
                allows comparison of metadata with different names but same data
                Default: HOST_SUBJECT_ID
    """

    #create default categories list if none passed
    if not categories:
        categories = ['HOST_SUBJECT_ID' for x in map_files]

    profiles = []
    #create a profile list for each mapping file, uisng category passed
    for map_file, category in zip(map_files, categories):
        result = make_profile_from_mapping(map_file, category)
        #append each resulting profile to final profile list
        for key in result:
            profiles.append(result[key])
    #normalize the profiles list before returning it
    return normalize_profiles(profiles)


def make_core_profile(map_files, categories=None):
    """ Wrapper function in case other calls are needed """
    return compare_profiles(get_profiles_list(map_files, categories))
