from cogent.util.unit_test import TestCase, main  #imports the test platform for Python
from profile import compare_profiles, normalize_profiles


class ProfileTests(TestCase):
    def setUp(self):
        self.not_shared_profiles = [{'taxa1': 0.20, 'taxa2': 0.30, 'taxa3': 0.15, 'taxa4': 0.35, 'not_shared': 0.00},
            {'taxa1': 0.10, 'taxa2': 0.50, 'taxa3': 0.15, 'taxa4': 0.25}]
        self.uneven_profiles = [{'taxa1': 0.20, 'taxa3': 0.30, 'taxa5': 0.15, 'taxa6': 0.35},
            {'taxa1': 0.10, 'taxa2': 0.50, 'taxa4': 0.15, 'taxa5': 0.05, 'taxa7': 0.20}]
        self.many_profiles = [{'taxa1': 0.20, 'taxa2': 0.30, 'taxa3': 0.15, 'taxa4': 0.35},
            {'taxa1': 0.10, 'taxa2': 0.50, 'taxa3': 0.15, 'taxa4': 0.25},
            {'taxa1': 0.15, 'taxa2': 0.22, 'taxa3': 0.15, 'taxa4': 0.48}]

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
        '''Make sure error raised when given an empty list or single profile'''
        #empty list check
        self.assertRaises(ValueError, compare_profiles, [])
        #single profile check
        self.assertRaises(ValueError, compare_profiles,
            [{'taxa1': 0.20, 'taxa2': 0.30}])

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




if __name__ == "__main__":
    main()
