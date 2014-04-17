#!/usr/bin/env python

__author__ = "Joshua Shorenstein"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Joshua Shorenstein"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "joshua.shorenstein@colorado.edu"
__status__ = "Development"

from unittest import TestCase, main
from json import loads
from os.path import dirname, abspath, join

from qiime.util import MetadataMap

from taxsim.collapse_metadata_maps import collapse_metadata_maps


class TestCollapseMetadataMaps(TestCase):
    def setUp(self):
        base = dirname(abspath(__file__))
        self.map1 = MetadataMap.parseMetadataMap(join(base, "support_files/"
                                                 "test_mapping.txt"))
        self.map2 = MetadataMap.parseMetadataMap(join(base, "support_files/"
                                                 "test_mapping2.txt"))
        self.map3 = MetadataMap.parseMetadataMap(join(base, "support_files/"
                                                 "test_mapping3.txt"))
        self.maplist = [self.map1, self.map2]

    def test_collapse_metadata_maps_sample_ids(self):
        """Makes sure samples from two studies with same id loaded uniquely"""
        pass

    def test_collapse_metadata_maps_taxa(self):
        """Makes sure all taxa are parsed out correctly"""
        collapsed = collapse_metadata_maps(self.maplist)
        tax_profile = collapsed.getCategoryValue(collapsed.SampleIds[0],
                                                 "TaxonomyProfile")
        obs_taxa = set(loads(tax_profile).keys())
        exp_taxa = set(["k_kingdom1", "k_kingdom2", "k_kingdom3",
                        "k_kingdom4", "not_shared"])
        self.assertEqual(exp_taxa, obs_taxa)

    def test_collapse_metadata_maps_metadata(self):
        """Makes sure all the metadata columns are parsed out correctly"""
        collapsed = collapse_metadata_maps(self.maplist)
        obs_columns = set(collapsed.CategoryNames)
        exp_columns = set(["HOST_SUBJECT_ID", "TaxonomyProfile"])
        self.assertEqual(exp_columns, obs_columns)

    def test_collapse_metadata_maps_profiles(self):
        """Makes sure Taxonomy Profile for samples are created correctly"""
        collapsed = collapse_metadata_maps(self.maplist)
        # build a dictionary of profiles
        obs_profiles = {}
        for sampleid in collapsed.SampleIds:
            taxaprofile = loads(collapsed.getCategoryValue(sampleid,
                                                           "TaxonomyProfile"))
            obs_profiles[sampleid] = taxaprofile
        exp_profiles = {'sid4':
                        {'k_kingdom1': 0.2, 'k_kingdom2': 0.5,
                         'k_kingdom3': 0.0, 'k_kingdom4': 0.3,
                         'not_shared': 0.0},
                        'sid5':
                        {'k_kingdom1': 0.5, 'k_kingdom2': 0.3,
                         'k_kingdom3': 0.0, 'k_kingdom4': 0.2,
                         'not_shared': 0.0},
                        'sid6':
                        {'k_kingdom1': 0.8, 'k_kingdom2': 0.1,
                         'k_kingdom3': 0.0, 'k_kingdom4': 0.1,
                         'not_shared': 0.0},
                        'sid1':
                        {'k_kingdom1': 0.2, 'k_kingdom3': 0.3,
                         'k_kingdom2': 0.5, 'k_kingdom4': 0.0,
                         'not_shared': 0.0},
                        'sid2':
                        {'k_kingdom1': 0.5, 'k_kingdom3': 0.2,
                         'k_kingdom2': 0.3, 'k_kingdom4': 0.0,
                         'not_shared': 0.0},
                        'sid3':
                        {'k_kingdom1': 0.3, 'k_kingdom3': 0.5,
                         'k_kingdom2': 0.2, 'k_kingdom4': 0.0,
                         'not_shared': 0.0}}
        self.assertEqual(exp_profiles, obs_profiles)

    def test_collapse_metadata_maps_spec_categories(self):
        """Make sure only specified categories are parsed out"""
        collapsed = collapse_metadata_maps(self.maplist, ["HOST_SUBJECT_ID"])
        obs_columns = collapsed.CategoryNames
        exp_columns = ["HOST_SUBJECT_ID", "TaxonomyProfile"]
        self.assertEqual(exp_columns, obs_columns)

    def test_collapse_metadata_maps_duplicate_sampleid(self):
        """Make sure error raised if duplicate sample ids found"""
        self.assertRaises(ValueError, collapse_metadata_maps,
                          [self.map1, self.map1])

    def test_collapse_metadata_maps_bad_float_conversion(self):
        """Make sure error raised if cannot convert taxa value to float"""
        self.assertRaises(ValueError, collapse_metadata_maps,
                          [self.map1, self.map3])

if __name__ == "__main__":
    main()
