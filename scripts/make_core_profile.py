#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from qiime.util import parse_command_line_parameters, make_option
from SCGM.profile import make_profile_from_mapping

script_info = {}
script_info['brief_description'] = """"""
script_info['script_description'] = """"""
script_info['script_usage'] = []
script_info['output_description'] = """"""
script_info['required_options'] = [
	make_option('-m', '--mapping_fp', type='existing_filepath',
		help="Mapping filepath result of summarize_taxa.py"),
	make_option('-c', '--category', type='string',
		help="Mapping file category")
]
script_info['optional_options'] = []
script_info['version'] = __version__

if __name__ == "__main__":
	option_parser, opts, args = parse_command_line_parameters(**script_info)
	result = make_profile_from_mapping(opts.mapping_fp)

	for sid in result:
		print sid
		print "\n"
		print result[sid]
