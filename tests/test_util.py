#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from os import remove, mkdir, rmdir
from os.path import join

from cogent.util.unit_test import TestCase, main
from qiime.util import get_tmp_filename, load_qiime_config

from SCGM.util import check_exist_filepaths


class UtilTest(TestCase):
    def setUp(self):
        # Get QIIME's temp dir
        self.qiime_config = load_qiime_config()
        self.tmp_dir = self.qiime_config['temp_dir'] or '/tmp/'

        self._paths_to_clean_up = []
        self._dirs_to_clean_up = []

    def tearDown(self):
        """Clean temp files"""
        map(remove, self._paths_to_clean_up)
        map(rmdir, self._dirs_to_clean_up)

    def _create_directory_structure(self, correct=True):
        """Creates a directory structure for check_exist_filepaths function

        Returns:
            base_dir: the base directory path
            mapping_fps: a list with the relative paths from base_dir to
                the created mapping files

        If correct=False, it adds one mapping file to the mapping_fps list that
            do not exists
        """
        base_dir = get_tmp_filename(tmp_dir=self.tmp_dir, suffix='')
        mkdir(base_dir)

        self._dirs_to_clean_up.append(base_dir)

        mapping_fps = []
        for i in range(5):
            mapping_fp = get_tmp_filename(tmp_dir='', suffix='.txt')
            mapping_fps.append(mapping_fp)
            path_to_create = join(base_dir, mapping_fp)
            f = open(path_to_create, 'w')
            f.close()
            self._paths_to_clean_up.append(path_to_create)

        if not correct:
            mapping_fps.append(get_tmp_filename(tmp_dir='', suffix='.txt'))

        return base_dir, mapping_fps

    def test_check_exist_filepaths_correct(self):
        """Does not raises an error in a correct folder structure"""
        base_dir, mapping_fps = self._create_directory_structure(correct=True)
        try:
            check_exist_filepaths(base_dir, mapping_fps)
        except ValueError:
            raise AssertionError("ValueError raised")

    def test_check_exist_filepaths_wrong(self):
        """Raises an error if a mapping file does not exists"""
        base_dir, mapping_fps = self._create_directory_structure(correct=False)
        self.assertRaises(ValueError, check_exist_filepaths, base_dir,
                          mapping_fps)

if __name__ == '__main__':
    main()
