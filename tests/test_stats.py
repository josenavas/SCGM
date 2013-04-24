#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from numpy import zeros
from cogent.util.unit_test import TestCase, main
from SCGM.stats import bootstrap_profiles, build_similarity_matrix, \
                        is_diagonal_matrix

class StatsTest(TestCase):
    def setUp(self):
        self.profiles_list = [
            {'taxa1': 0.20, 'taxa2': 0.30, 'taxa3': 0.15, 'taxa4': 0.35},
            {'taxa1': 0.10, 'taxa2': 0.50, 'taxa3': 0.15, 'taxa4': 0.25},
            {'taxa1': 0.15, 'taxa2': 0.22, 'taxa3': 0.15, 'taxa4': 0.48}]

    def test_bootstrap_profiles(self):
        randfunc = lambda : 1
        obs_prof, obs_mean, obs_stdev, obs_ci = \
                    bootstrap_profiles(self.profiles_list, randfunc = randfunc)

        exp_prof = {'taxa1': (0.10),'taxa2': (0.22),
                    'taxa3': (0.15),'taxa4': (0.25)}
        

    def test_build_similarity_matrix(self):
        pass

    def test_is_diagonal_matrix_true(self):
        matrix = zeros([5, 5], dtype='4float64')
        for i in range(5):
            matrix[i][i] = (1.0, 0.0, 0.0, 0.0)

        self.assertTrue(is_diagonal_matrix(matrix))

    def test_is_diagonal_matrix_false(self):
        matrix = zeros([5, 5], dtype='4float64')
        for i in range(5):
            matrix[i][i] = (1.0, 0.0, 1.0, 1.0)
        matrix[0][3] = (1.0, 0.0, 1.0, 1.0)
        matrix[3][0] = (1.0, 0.0, 1.0, 1.0)

        self.assertFalse(is_diagonal_matrix(matrix))

if __name__ == '__main__':
    main()