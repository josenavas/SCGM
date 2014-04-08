#!/usr/bin/env python
from __future__ import division

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, TaxSim project"
__credits__ = ["Jose Antonio Navas Molina", "Joshua Shorenstein"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from itertools import izip
from collections import defaultdict
from json import dumps

from qiime.util import MetadataMap

from taxsim.profile import normalize_profiles


def collapse_metadata_maps(metadata_maps, categories=None):
    """
    Parameters
    ----------
    metadata_maps : list of MetadataMap
        The metadata map object to collapse in a single metadata map
    categories : list of strings
        The
    """
    if categories:
        categories = set(categories)
    else:
        # Get the categories that does not represent taxonomy
        categories = set([cat for cat in metadata_maps[0].CategoryNames
                          if not cat.startswith('k_')])
        # Get the common categories across all metadata maps
        for metamap in metadata_maps[1:]:
            categories = categories.intersection(metamap.CategoryNames)

    # Get all the taxonomies present in all the metadata maps
    taxonomies = set([cat for cat in metamap.CategoryNames
                      if cat.startswith('k_') for metamap in metadata_maps])

    sample_metadata = defaultdict(dict)
    profiles = defaultdict(dict)
    # Loop through all the metadata maps
    for metamap in metadata_maps:
        # Get the samples from the current metadata map
        sample_ids = metamap.SampleIds
        # Loop through all the categories that should be included
        # in the collapsed metadata map
        for category in categories:
            try:
                values = metamap.getCategoryValues(sample_ids, category)
            except KeyError:
                values = [None] * len(sample_ids)
            for sid, value in izip(sample_ids, values):
                sample_metadata[sid][category] = value
        # Loop through all the taxonomies that should be included in
        # the collapsed metadata map
        for taxa in taxonomies:
            try:
                taxa_vals = metamap.getCategoryValues(sample_ids, taxa)
            except KeyError:
                taxa_vals = [0.0] * len(sample_ids)
            for sid, tv in izip(sample_ids, taxa_vals):
                profiles[sid][taxa] = tv
    # Normalize profiles
    normalize_profiles(profiles)
    # Add the taxonomy profiles to each sample
    for sid in sample_metadata:
        sample_metadata[sid]['TaxonomyProfile'] = dumps(profiles[sid],
                                                        separators=(',', ':'))

    return MetadataMap(sample_metadata, "")
