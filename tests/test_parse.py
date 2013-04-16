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
from SCGM.parse import parse_mapping_table

class ParseTest(TestCase):
	def setUp(self):
		self.map_table_correct = correct_mapping_table.splitlines()
		self.map_table_no_header = no_header_mapping_table.splitlines()
		self.map_table_header_space = space_header_mapping_table.splitlines()
		self.map_table_data_space = space_data_mapping_table.splitlines()
		self.map_table_bad_1 = bad_mapping_table_1.splitlines()
		self.map_table_bad_2 = bad_mapping_table_2.splitlines()

	def test_parse_mapping_table(self):
		"""Successfully parses a correct mapping table file"""
		obs_headers, obs_dict = parse_mapping_table(self.map_table_correct)
		exp_headers = ['header1', 'header2', 'header3', 'header4']
		exp_dict = {
			'some/path/to/mapping_1.txt': {
				'header1' : 'h1_v1',
				'header2' : 'h2_v1',
				'header3' : 'h3_v1',
				'header4' : 'h4_v1',
			},
			'some/path/to/mapping_2.txt': {
				'header1' : 'h1_v2',
				'header2' : 'h2_v1',
				'header3' : 'h3_v2',
				'header4' : 'h4_v1',
			},
			'some/path/to/mapping_3.txt': {
				'header1' : 'h1_v3',
				'header2' : 'h2_v2',
				'header3' : 'h3_v1',
				'header4' : 'h4_v2',
			}
		}
		self.assertEqual(obs_headers, exp_headers)
		self.assertEqual(obs_dict, exp_dict)

	def test_parse_mapping_table_no_header(self):
		"""Raises an error when a mapping table without header is passed"""
		self.assertRaises(ValueError, parse_mapping_table,
			self.map_table_no_header)

	def test_parse_mapping_table_space_header(self):
		"""Raises an error when the mapping table header is space delimited"""
		self.assertRaises(ValueError, parse_mapping_table,
			self.map_table_header_space)

	def  test_parse_mapping_table_space_data(self):
		"""Raises an error when the mapping table data is space delimited"""
		self.assertRaises(ValueError, parse_mapping_table,
			self.map_table_data_space)

	def test_parse_mapping_table_bad(self):
		"""Raises an error if the number of values and headers are not equal"""
		self.assertRaises(ValueError, parse_mapping_table,
			self.map_table_bad_1)

		self.assertRaises(ValueError, parse_mapping_table,
			self.map_table_bad_2)

correct_mapping_table="""#mapping_fp\theader1\theader2\theader3\theader4
# This is a comment line
# Comment lines should be ignored
some/path/to/mapping_1.txt\th1_v1\th2_v1\th3_v1\th4_v1
some/path/to/mapping_2.txt\th1_v2\th2_v1\th3_v2\th4_v1
some/path/to/mapping_3.txt\th1_v3\th2_v2\th3_v1\th4_v2"""

no_header_mapping_table="""#This\tlooks\ta\theader\tline
# But it should start with mapping_fp
some/path/to/mapping_1.txt\th1_v1\th2_v1\th3_v1\th4_v1
some/path/to/mapping_2.txt\th1_v2\th2_v1\th3_v2\th4_v1
some/path/to/mapping_3.txt\th1_v3\th2_v2\th3_v1\th4_v2"""

space_header_mapping_table="""#mapping_fp header1 header2 header3 header4
# This looks like a correct mapping table file
# but the header are space delimited instead of tab delimited
some/path/to/mapping_1.txt\th1_v1\th2_v1\th3_v1\th4_v1
some/path/to/mapping_2.txt\th1_v2\th2_v1\th3_v2\th4_v1
some/path/to/mapping_3.txt\th1_v3\th2_v2\th3_v1\th4_v2"""

space_data_mapping_table="""#mapping_fp\theader1\theader2\theader3\theader4
# Looks correct, but the data is space delimited insted of 
# tab delimited
some/path/to/mapping_1.txt h1_v1 h2_v1 h3_v1 h4_v1
some/path/to/mapping_2.txt h1_v2 h2_v1 h3_v2 h4_v1
some/path/to/mapping_3.txt h1_v3 h2_v2 h3_v1 h4_v2"""

bad_mapping_table_1="""#mapping_fp\theader1\theader2\theader3\theader4
# This is a comment line
# Comment lines should be ignored
some/path/to/mapping_1.txt\th1_v1\th2_v1\th3_v1\th4_v1
some/path/to/mapping_2.txt\th1_v2\th2_v1\th3_v2
some/path/to/mapping_3.txt\th1_v3\th2_v2\th3_v1\th4_v2"""

bad_mapping_table_2="""#mapping_fp\theader1\theader2\theader3\theader4
# This is a comment line
# Comment lines should be ignored
some/path/to/mapping_1.txt\th1_v1\th2_v1\th3_v1\th4_v1
some/path/to/mapping_2.txt\th1_v2\th2_v1\th3_v2 h4_v1
some/path/to/mapping_3.txt\th1_v3\th2_v2\th3_v1\th4_v2"""

if __name__ == '__main__':
	main()