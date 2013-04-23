#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

def parse_mapping_table(lines):
	"""Parses a mapping table file

	Input:
		lines: the mapping table file object

	Returns:
		headers: a list with the mapping table headers except the
			'mapping_fp'
		data: a dictionary keyed by mapping file path where values are
			dictionaries keyed by header and values are the translated header in
			that mapping file
	"""
	headers = []
	data = {}

	for line in lines:
		if line:
			# Check if it is the header line
			if line.startswith('#mapping_fp'):
				if '\t' not in line:
					raise ValueError, "Header line is not tab delimited"
				headers = line.strip().split('\t')[1:]
			# Check if the line is a comment
			elif line.startswith('#'):
				continue
			else:
				if len(headers) == 0:
					raise ValueError, "Header line not found. It starts with "+\
						"#mapping_fp?"
				if '\t' not in line:
					raise ValueError, "One of more of the data lines are not"+\
						"tab delimited"
				values = line.strip().split('\t')
				mapping_path = values[0]
				values = values[1:]
				if len(headers) != len(values):
					raise ValueError, "The number of headers and the number "+\
						"of values per row should be the same"
				map_values = {}
				for i in range(len(headers)):
					map_values[headers[i]] = values[i]
				data[mapping_path] = map_values

	return headers, data