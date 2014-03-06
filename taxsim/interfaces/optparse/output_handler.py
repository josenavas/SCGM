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

from os.path import exists

from pyqi.core.exception import IncompetentDeveloperError


def write_metadata_map(result_key, data, option_value=None):
    """"""
    if option_value is None:
        raise IncompetentDeveloperError("Cannot write output without a "
                                        "filepath.")
    if exists(option_value):
        raise IOError("Output path '%s' already exists." % option_value)

    with open(option_value, 'w') as f:
        headers = data.CategoryNames
        headers.remove('SampleIds')
        f.write("#SapleIds\t%s\n" % '\t'.join(headers))
        f.write("#%s\n" % data.Comments)
        for sid in data.SampleIds:
            values = [data.getCategoryValue(sid, h) for h in headers]
            f.write("%s\t%s\n" % (sid, '\t'.join(values)))
