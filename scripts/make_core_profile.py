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
from SCGM.core import make_core_profile

script_info = {}
script_info['brief_description'] = """"""
script_info['script_description'] = """"""
script_info['script_usage'] = []
script_info['output_description'] = """"""
script_info['required_options'] = [
    make_option('-m', '--mapping_fps', type='existing_filepaths',
        help="Mapping filepaths result of summarize_taxa.py"),
]
script_info['optional_options'] = [
    make_option('-c', '--categories', type='string',
        default=None,
        help="Mapping file categories"),
]
script_info['version'] = __version__

if __name__ == "__main__":
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    map_files = opts.mapping_fps

    categories = None

    if opts.categories:
        categories = opts.categories.split(',')

        if len(map_files) != len(categories):
            raise ValueError, "Must supply a category for each mapping file"

    lista = make_core_profile(map_files, categories)

    for l in lista:
        print l
