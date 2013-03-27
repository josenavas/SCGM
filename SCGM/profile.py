from qiime.parse import parse_mapping_file_to_dict
from qiime.filter import sample_ids_from_metadata_description

def normalize_profiles(profiles):
    """Make sure all profiles contain the same taxa keys"""
    if len(profiles) == 0:
        raise ValueError, "An empty profiles list cannot be normalized"
    if len(profiles) == 1:
        raise ValueError, "More than one profile is needed to normalized"
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

def compare_profiles(profiles):
    """Compare the keys for profile 1 and profile 2 and take the minimum value"""
    if len(profiles) == 0:
        raise ValueError, "Cannot compare an empty list"
    if len(profiles) == 1:
        raise ValueError, "Cannot compare only one profile"
    result = {}
    share = 0.0
    #Start with the first taxa key of the profiles
    for key in profiles[0]:
        if key == "not_shared":
            continue
        #Find the minimum for the given taxa unit in the profiles
        result[key] = min([prof[key] for prof in profiles])
        share += result[key]
    result['not_shared'] = 1.0 - share
    return result

def make_profile(map_data, sids):
    profiles = []
    for sid in sids:
        profile = {}
        for key in map_data[sid]:
            if key.startswith('k_'):
                profile[key] = float(map_data[sid][key])
        profiles.append(profile)

    if len(profiles) == 1:
        profiles[0]['not_shared'] = 0.0
        return profiles[0]

    return compare_profiles(normalize_profiles(profiles))

def make_profile_from_mapping(mapping_fp, category="HOST_SUBJECT_ID"):
    map_f = open(mapping_fp, 'U')
    mapping_data, comments = parse_mapping_file_to_dict(map_f)
    map_f.close()

    values = set([mapping_data[sid][category] for sid in mapping_data])

    result = {}
    for value in values:
        map_f = open(mapping_fp, 'U')
        sids = sample_ids_from_metadata_description(map_f, category+":"+value)
        map_f.close()

        result[value] = make_profile(mapping_data, sids)

    return result