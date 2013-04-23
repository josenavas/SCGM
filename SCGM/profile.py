#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Jose Antonio Navas Molina", "Joshua Shorenstein",
                "Elizabeth Lor"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from qiime.parse import parse_mapping_file_to_dict
from qiime.filter import sample_ids_from_metadata_description

def normalize_profiles(profiles):
    """Make sure all profiles contain the same taxa keys

        profiles: list of sample profiles
    """
    if len(profiles) == 0:
        raise ValueError, "An empty profiles list cannot be normalized"
    if len(profiles) == 1:
        raise ValueError, "More than one profile is needed to normalize"

    #Make a set of taxa keys for each profiles
    taxa = set([key for prof in profiles for key in prof.keys()])
    if 'not_shared' not in taxa:
        #Add the 'not_shared' in the taxa
        taxa.add('not_shared')

    for key in taxa:
        for profile in profiles:
            if key not in profile:
                #If the taxa key is not in the profile, set it equal to 0.0
                profile[key] = 0.0
    return profiles

def compare_profiles(profiles, normalize=False):
    """ Compare the keys over all profiles and take the minimum value

        profiles: list of profiles
        normalize: if True, the profiles will be normalized before comparison
    """
    if len(profiles) == 0:
        raise ValueError, "Cannot compare an empty list"
    if len(profiles) == 1:
        raise ValueError, "Cannot compare only one profile"
    if normalize:
        profiles = normalize_profiles(True)
    result = {}
    share = 0.0
    #Start with the first taxa key of the profiles
    for key in profiles[0]:
        #Skip the not_shared taxa, since is artificially added
        if key == "not_shared":
            continue
        #Find the minimum for the given taxa unit in the profiles
        result[key] = min([prof[key] for prof in profiles])
        share += result[key]
    #Add the not_shared unit as remaining precentage to sum to 100%
    result['not_shared'] = 1.0 - share
    return result

def make_profile_by_sid(map_data, sid, taxa_level):
    """ Create a profile for the sample ID passed 
    Inputs
        map_data: mapping file data from parse_mapping_file_to_dict()
        sid: the sample ID
    """
    profile = {}
    #loop over the keys in the mapping file
    for key in map_data[sid]:
        #all keys with taxa data start with k_
        if key.startswith('k_') and len(key.split(';')) == taxa_level:
            profile[key] = float(map_data[sid][key])
    # Add the 'not_shared' key in order to normalize this profile
    profile['not_shared'] = 0.0
    return profile

def make_profiles_by_category(mapping_fp, taxa_level, category):
    """ Creates a list of profiles for each unique value in the category
    Inputs:
        mapping_fp: filepath to the mapping file
        category: mapping file category to split data over
                  defaults to HOST_SUBJECT_ID
    Returns a dictionary keyed by the values on that category and a list of 
        profiles as values
    """
    # Parse the mapping file
    map_f = open(mapping_fp, 'U')
    mapping_data, comments = parse_mapping_file_to_dict(map_f)
    map_f.close()
    # Get a list of unique keys for the specified category
    if category == 'SampleID':
        result = {}
        for sid in mapping_data:
            result[sid] = [make_profile_by_sid(mapping_data, sid, taxa_level)]
    else:
        values = set([mapping_data[sid][category] for sid in mapping_data])
        result = {}
        # Loop over each value in that category
        for value in values:
            # Re-open the mapping file
            map_f = open(mapping_fp, 'U')
            # Get sample ids that match the value
            sids = sample_ids_from_metadata_description(map_f,
                                                        category+":"+value)
            map_f.close()
            # Create the list with all the profiles of the sample IDs in this
            # category value
            result[value] = [make_profile_by_sid(mapping_data,
                                                sid, taxa_level) for sid in sids]
    return result

def write_profile(profile, output_fp):
    """ Writes the profile to the file output_fp

    Inputs:
        profile: the profile to be written
        output_fp: the output filepath
    """
    outf = open(output_fp, 'w')
    sorted_keys = sorted(profile.keys())
    for k in sorted_keys:
            value = profile[k]
            outf.write('\t'.join([k, str(value)]) + '\n')
    outf.close()