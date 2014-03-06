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


class GradientTest(Command):
    BriefDescription = "FILL IN A 1 SENTENCE DESCRIPTION"
    LongDescription = "GO INTO MORE DETAIL"
    CommandIns = ParameterCollection([
        CommandIn(Name='foo', DataType=str,
                  Description='some required parameter', Required=True),
        CommandIn(Name='bar', DataType=int,
                  Description='some optional parameter', Required=False,
                  Default=1)
    ])

    CommandOuts = ParameterCollection([
        CommandOut(Name="result_1", DataType=str, Description="xyz"),
        CommandOut(Name="result_2", DataType=str, Description="123"),
    ])

    def run(self, **kwargs):
        # EXAMPLE:
        # return {'result_1': kwargs['foo'] * kwargs['bar'],
        #         'result_2': "Some output bits"}
        raise NotImplementedError("You must define this method")

CommandConstructor = GradientTest
