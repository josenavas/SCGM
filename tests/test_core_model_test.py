#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from os import remove, rmdir
from unittest import TestCase, main

from SCGM.core_model_test import core_model_test


class CoreModelTestTest(TestCase):
    def setUp(self):
        """"""

    def tearDown(self):
        """ Clean temp files"""
        map(remove, self._paths_to_clean_up)
        map(rmdir, self._dirs_to_clean_up)

    def test_core_model_test(self):
        pass

    def test_get_profiles_list(self):
        pass

if __name__ == '__main__':
    main()
