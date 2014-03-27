#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from collections import namedtuple
from json import loads

from taxsim.stats import bootstrap_profiles

CoreResults = namedtuple('CoreResults', ('model', 'profile', 'mean',
                                         'stdev', 'ci'))


def core_model_test(taxa_map, taxa_level, alpha=0.05, repetitions=1000):
    """ Tests the core model

    Parameters
    ----------
    taxa_map : MetadataMap
        Mapping file with the normalized taxonomy profiles
    taxa_level : int
        The taxa level to test
    alpha: float, optional
        Alpha value used to calculate the level of confidence 1-alpha. Default:
        0.05
    repetitions: int, optional
        Number of bootstrap repetitions. Default: 1000

    Returns
    -------
    CoreResults
        The results of testing the core model
    """
    # Get the profiles
    profiles = [loads(value) for value in
                taxa_map.getCategoryValues(taxa_map.SampleIds,
                                           "TaxonomyProfile")]
    # Test the core model
    profile, mean, stdev, ci = bootstrap_profiles(profiles)
    # Check which model is found
    if profile['not_shared'] < 0.5:
        model = "Substantial core"
    elif profile['not_shared'] < 1.0:
        model = "Minimal core"
    else:
        model = "No core"
    return CoreResults(model, profile, mean, stdev, ci)
