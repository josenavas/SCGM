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

from taxsim.core_model_test import core_model_test, CoreResults


class CoreTest(Command):
    BriefDescription = ("FILL IN A 1 SENTENCE DESCRIPTION")
    LongDescription = ("GO INTO MORE DETAIL")
    CommandIns = ParameterCollection([
        CommandIn(Name='taxa_summary_map', DataType=MetadataMap,
                  Description='MetadataMap object containing the taxonomy '
                              'profile (e.g. output of SummarizeTaxaCollapser',
                  Required=True),
        CommandIn(Name='level', DataType=int,
                  Description="The taxa level to test")
    ])

    CommandOuts = ParameterCollection([
        CommandOut(Name="result", DataType=CoreResults,
                   Description="The results of evaluating the core mode on "
                               "the input data")
    ])

    def run(self, **kwargs):
        summary_map = kwargs['taxa_summary_map']
        level = kwargs['level']

        res = core_model_test()

        return {'result': res}

CommandConstructor = CoreTest