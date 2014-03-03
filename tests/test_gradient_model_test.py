#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from qiime.util import TestCase, main

from SCGM.gradient_model_test import gradient_model_test


class GradientModelTestTest(TestCase):
    def setUp(self):
        raise ValueError("Test not implemented!!!")

if __name__ == '__main__':
    main()
