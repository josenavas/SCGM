#!/usr/bin/env python
from __future__ import division

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, TaxSim project"
__credits__ = ["Jose Antonio Navas Molina", "Joshua Shorenstein"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from pyqi.core.interfaces.optparse import (OptparseUsageExample,
                                           OptparseOption, OptparseResult)
from pyqi.core.command import (make_command_in_collection_lookup_f,
                               make_command_out_collection_lookup_f)
from pyqi.core.interfaces.optparse.input_handler import string_list_handler

from taxsim.commands.summarize_taxa_collapser import CommandConstructor
from taxsim.interfaces.optparse.input_handler import metadata_map_list_handler
from taxsim.interfaces.optparse.output_handler import write_metadata_map

# Convenience function for looking up parameters by name.
cmd_in_lookup = make_command_in_collection_lookup_f(CommandConstructor)
cmd_out_lookup = make_command_out_collection_lookup_f(CommandConstructor)

usage_examples = [
    OptparseUsageExample(ShortDesc="",
                         LongDesc="",
                         Ex="%prog --foo --bar some_file")
]

inputs = [
    OptparseOption(Parameter=cmd_in_lookup('categories'),
                   Type=str,
                   Action='store',
                   Handler=string_list_handler,
                   ShortName='c',
                   Name='categories',
                   Required=False,
                   Help='Comma-separated list of categories to include in the '
                        'collapsed metadata map',
                   Default=None,
                   ),
    OptparseOption(Parameter=cmd_in_lookup('metadata_maps'),
                   Type='existing_filepaths',
                   Action='store',
                   Handler=metadata_map_list_handler,
                   ShortName='m',
                   Name='metadata_maps',
                   Required=True,
                   Help='Comma-separated list of metadata maps filepaths with '
                        'the taxonomy information included (e.g. result from '
                        'summarize_taxa.py',
                   ),
    OptparseOption(Parameter=None,
                   Type='new_filepath',
                   Action='store',
                   Handler=None,
                   ShortName='o',
                   Name='output-fp',
                   Required=True,
                   Help='Output collapsed metadata map filepath')
]

outputs = [
    OptparseResult(Parameter=cmd_out_lookup('collapsed_map'),
                   Handler=write_metadata_map,
                   InputName='output-fp'),
]
