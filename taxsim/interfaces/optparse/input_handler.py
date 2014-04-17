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

from qiime.util import MetadataMap
from qiime.parse import parse_mapping_file_to_dict


def metadata_map_list_handler(metadata_map_fps):
    """"""
    for metamap_fp in metadata_map_fps:
        with open(metamap_fp, 'U') as metamap_f:
            map_data, comments = parse_mapping_file_to_dict(metamap_f,
                                                            strip_quotes=False)
            yield MetadataMap(map_data, comments)
