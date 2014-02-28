#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from os import remove
from os.path import exists

from qiime.util import load_qiime_config

from cogent.util.unit_test import TestCase, main
from SCGM.matplotlib_pie import plot_pie


class PieTest(TestCase):
    def setUp(self):
        # Get QIIME's temp dir
        self.qiime_config = load_qiime_config()
        self.tmp_dir = self.qiime_config['temp_dir'] or '/tmp/'
        self.data = [0.1336206897, 0.2740524781, 0.5923268322]
        self.labels = ['o__Bacteroidales', 'o__Clostridiales', 'not_shared']

        self._paths_to_clean_up = []

    def tearDown(self):
        """Clean temp files"""
        map(remove, self._paths_to_clean_up)

    def test_plot_pie_png_no_labels(self):
        """Make sure something is generated for png"""
        outpath = self.tmp_dir + "testpie.png"
        plot_pie(self.data, outpath)
        assert exists(outpath)
        self._paths_to_clean_up.append(outpath)

    def test_plot_pie_pdf_no_labels(self):
        """Make sure something is generated for pdf"""
        outpath = self.tmp_dir + "testpie.pdf"
        plot_pie(self.data, outpath)
        assert exists(outpath)
        self._paths_to_clean_up.append(outpath)

    def test_plot_pie_labels(self):
        """Make sure something is generated with labels included"""
        outpath = self.tmp_dir + "testpie.png"
        plot_pie(self.data, outpath, self.labels)
        assert exists(outpath)
        self._paths_to_clean_up.append(outpath)

    def test_plot_pie_title(self):
        """Make sure something is generated with title included"""
        outpath = self.tmp_dir + "testpie.png"
        plot_pie(self.data, outpath, plot_title="testgraph")
        assert exists(outpath)
        self._paths_to_clean_up.append(outpath)

    def test_plot_pie_bad_extension(self):
        """Make sure ValueError raised with bad extension"""
        outpath = self.tmp_dir + "testpie.jpg"
        self.assertRaises(ValueError, plot_pie, self.data, outpath)

    def test_plot_pie_label_len_mismatch(self):
        """Make suer RuntimeError raised when len(data) != len(labels)"""
        outpath = self.tmp_dir + "testpie.png"
        self.assertRaises(RuntimeError, plot_pie, self.data, outpath, [""])


if __name__ == "__main__":
    main()
