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

from pyqi.core.command import (Command, CommandIn, CommandOut,
                               ParameterCollection)
from qiime.util import MetadataMap
from taxsim.collapse_metadata_maps import collapse_metadata_maps


class SummarizeTaxaCollapser(Command):
    BriefDescription = ("Collapses the results of summarize taxa of multiple "
                        "studies")
    LongDescription = ("Given the metadata map objects result from summarize "
                       "taxa, generates a collapsed metadata map with the "
                       "common metadata categories or with the categories "
                       "provided.")
    CommandIns = ParameterCollection([
        CommandIn(Name='metadata_maps', DataType=list,
                  Description='List of metadata maps objects with the taxonomy'
                              ' information included', Required=True),
        CommandIn(Name='categories', DataType=list,
                  Description='Categories to include in the collapsed '
                              'metadata map',
                  Required=False, Default=None)
    ])

    CommandOuts = ParameterCollection([
        CommandOut(Name="collapsed_map", DataType=MetadataMap,
                   Description="The collapsed metadata map"),
    ])

    def run(self, **kwargs):
        metadata_maps = kwargs['metadata_maps']
        categories = kwargs['categories']

        collapsed_map = collapse_metadata_maps(metadata_maps, categories)

        return {'collapsed_map': collapsed_map}

CommandConstructor = SummarizeTaxaCollapser
