#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from cogent.util.unit_test import TestCase, main
from qiime.util import get_tmp_filename, load_qiime_config
from os import remove, rmdir
from SCGM.core_model_test import core_model_test, get_profiles_list

class CoreModelTestTest(TestCase):
    def setUp(self):
        # Get QIIME's temp dir
        self.qiime_config = load_qiime_config()
        self.tmp_dir = self.qiime_config['temp_dir'] or '/tmp/'

        self._paths_to_clean_up = []
        self._dirs_to_clean_up = []
        raise ValueError, "Test not implemented!!!"

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