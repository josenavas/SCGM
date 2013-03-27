#!/usr/bin/env python

__author__ = "Joshua Shorenstein"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Joshua Shorenstein","Elizabeth Lor","Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Joshua Shorenstein"
__email__ = "jshorens@gmail.com"
__status__ = "Development"


from cogent.util.unit_test import TestCase, main
from SCGM.profile import compare_profiles, normalize_profiles, make_profile, make_profile_from_mapping
from StringIO import StringIO


class ProfileTests(TestCase):
    def setUp(self):
        self.not_shared_profiles = [{'taxa1': 0.20, 'taxa2': 0.30, 'taxa3': 0.15, 'taxa4': 0.35, 'not_shared': 0.00},
            {'taxa1': 0.10, 'taxa2': 0.50, 'taxa3': 0.15, 'taxa4': 0.25}]
        self.uneven_profiles = [{'taxa1': 0.20, 'taxa3': 0.30, 'taxa5': 0.15, 'taxa6': 0.35},
            {'taxa1': 0.10, 'taxa2': 0.50, 'taxa4': 0.15, 'taxa5': 0.05, 'taxa7': 0.20}]
        self.many_profiles = [{'taxa1': 0.20, 'taxa2': 0.30, 'taxa3': 0.15, 'taxa4': 0.35},
            {'taxa1': 0.10, 'taxa2': 0.50, 'taxa3': 0.15, 'taxa4': 0.25},
            {'taxa1': 0.15, 'taxa2': 0.22, 'taxa3': 0.15, 'taxa4': 0.48}]
        self.map_data = {
            'sid1':{'HOST_SUBJECT_ID':'hsid_1',
                    'map_h':'value1',
                    'k_kingdom1': '0.2',
                    'k_kingdom2': '0.5',
                    'k_kingdom3': '0.3',},
            'sid2':{'HOST_SUBJECT_ID':'hsid_2',
                    'map_h':'value1',
                    'k_kingdom1': '0.5',
                    'k_kingdom2': '0.3',
                    'k_kingdom3': '0.2',},
            'sid3':{'HOST_SUBJECT_ID':'hsid_3',
                    'map_h':'value2',
                    'k_kingdom1': '0.3',
                    'k_kingdom2': '0.2',
                    'k_kingdom3': '0.5',}}
        self.mapping_fp = "./support_files/test_mapping.txt"

    def test_compare_profiles(self):
        ''' Comparing three profiles, testing when each are the min and when one \
        taxa is equal '''
        result = compare_profiles(self.many_profiles)
        exresult = {'taxa1': 0.10, 'taxa2': 0.22, 'taxa3': 0.15, 'taxa4': 0.25, 
            'not_shared': 0.28}
        #make sure the keys in each are the same
        self.assertEquals(set(result.keys()), set(exresult.keys()))
        #make sure the values are correct-ish
        for key in result:
            self.assertAlmostEquals(result[key], exresult[key])

    def test_compare_profiles_fail(self):
        '''Make sure error raised when given an empty list or a single profile'''
        #empty list check
        self.assertRaises(ValueError, compare_profiles, [])
        #single profile check
        self.assertRaises(ValueError, compare_profiles, [{'taxa1': 0.20, 'taxa2': 0.30}])

    def test_normalize_profiles_fail(self):
        '''Make sure error raised when given an empty list or single profile'''
        #empty list check
        self.assertRaises(ValueError, normalize_profiles, [])
        #single profile check
        self.assertRaises(ValueError, normalize_profiles,
            [{'taxa1': 0.20, 'taxa2': 0.30}])

    def test_normalize_profiles_eq_len(self):
        '''Normalizing two profiles of equal length'''
        self.assertEquals(normalize_profiles(self.many_profiles),
            [{'taxa1': 0.20, 'taxa2': 0.30, 'taxa3': 0.15, 'taxa4': 0.35, 'not_shared': 0.00},
            {'taxa1': 0.10, 'taxa2': 0.50, 'taxa3': 0.15, 'taxa4': 0.25, 'not_shared': 0.00},
            {'taxa1': 0.15, 'taxa2': 0.22, 'taxa3': 0.15, 'taxa4': 0.48, 'not_shared': 0.00}])

    def test_normalize_profiles_neq_len(self):
        '''Normalizing two profiles with many diferent taxa'''
        self.assertEquals(normalize_profiles(self.uneven_profiles),
            [{'taxa1': 0.20, 'taxa2': 0.00, 'taxa3': 0.30, 'taxa4': 0.00, 'taxa5': 0.15, 'taxa6': 0.35, 'taxa7': 0.00, 'not_shared': 0.00},
            {'taxa1': 0.10, 'taxa2': 0.50, 'taxa3': 0.00, 'taxa4': 0.15, 'taxa5': 0.05, 'taxa6': 0.00, 'taxa7': 0.20, 'not_shared': 0.00}])

    def test_compare_profiles_not_shared(self):
        '''Normalizing with one profile containing not_shared and one without'''
        result = compare_profiles(self.not_shared_profiles)
        exresult = {'taxa1': 0.10, 'taxa2': 0.30, 'taxa3': 0.15, 'taxa4': 0.25, 'not_shared': 0.20}
        #make sure the keys in each are the same
        self.assertEquals(set(result.keys()), set(exresult.keys()))
        #make sure the values are correct-ish
        for key in result:
            self.assertAlmostEquals(result[key], exresult[key])

    def test_make_profile(self):
        sids = ['sid1']
        obs = make_profile(self.map_data, sids)
        exp = {
            'k_kingdom1': 0.2,
            'k_kingdom2': 0.5,
            'k_kingdom3': 0.3,
            'not_shared': 0.0}
        self.assertEquals(obs, exp)

        sids = ['sid2']
        obs = make_profile(self.map_data, sids)
        exp = {
            'k_kingdom1': 0.5,
            'k_kingdom2': 0.3,
            'k_kingdom3': 0.2,
            'not_shared': 0.0}
        self.assertEquals(obs, exp)

        sids = ['sid3']
        obs = make_profile(self.map_data, sids)
        exp = {
            'k_kingdom1': 0.3,
            'k_kingdom2': 0.2,
            'k_kingdom3': 0.5,
            'not_shared': 0.0}
        self.assertEquals(obs, exp)

        sids = ['sid1', 'sid2']
        obs = make_profile(self.map_data, sids)
        exp = {
            'k_kingdom1': 0.2,
            'k_kingdom2': 0.3,
            'k_kingdom3': 0.2,
            'not_shared': 0.3}
        self.assertEquals(obs.keys(), exp.keys())
        for key in obs:
            self.assertAlmostEquals(obs[key], exp[key])

    def test_make_profile_from_mapping(self):
        obs = make_profile_from_mapping(self.mapping_fp)
        exp = {
            'hsid_1' : {
                'k_kingdom1': 0.2,
                'k_kingdom2': 0.5,
                'k_kingdom3': 0.3,
                'not_shared': 0.0},
            'hsid_2' : {
                'k_kingdom1': 0.5,
                'k_kingdom2': 0.3,
                'k_kingdom3': 0.2,
                'not_shared': 0.0},
            'hsid_3' : {
                'k_kingdom1': 0.3,
                'k_kingdom2': 0.2,
                'k_kingdom3': 0.5,
                'not_shared': 0.0}
        }
        self.assertEquals(obs, exp)

        obs = make_profile_from_mapping(self.mapping_fp, "map_h")
        exp = {
            'value1' : {
                'k_kingdom1': 0.2,
                'k_kingdom2': 0.3,
                'k_kingdom3': 0.2,
                'not_shared': 0.3},
            'value2' : {
                'k_kingdom1': 0.3,
                'k_kingdom2': 0.2,
                'k_kingdom3': 0.5,
                'not_shared': 0.0}
        }
        self.assertEquals(obs.keys(), exp.keys())
        for k1 in exp:
            self.assertEquals(obs[k1].keys(), exp[k1].keys())
            for k2 in exp[k1]:
                self.assertAlmostEquals(obs[k1][k2], exp[k1][k2])

if __name__ == "__main__":
    main()
