#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Jose Antonio Navas Molina", "Joshua Shorenstein", "Elizabeth Lor"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from SCGM.profile import make_profile_from_mapping, normalize_profiles

def get_profiles_list(map_files, categories=None):
	if not categories:
		categories = ['HOST_SUBJECT_ID' for x in map_files]

	profiles = []

	for map_file, category in zip(map_files, categories):
		result = make_profile_from_mapping(map_file, category)
		for key in result:
			profiles.append(result[key])

	return normalize_profiles(profiles)


def make_core_profile(map_files, categories=None):
	return get_profiles_list(map_files, categories)