#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

VALID_MODELS = ['core', 'gradient', 'subpopulation']

from SCGM.parse import parse_mapping_table
from SCGM.util import check_exist_filepaths, sort_category_values

def microbiome_model_test(base_dir, lines, models, category, sort, output_dir):
    """
    Inputs:
        lines: mapping table file lines
        models: list of models to test
        category: category to use in the gradient or subpopulation models
        sort: list of category values sorted, or 'ascendant' or 'descendant'
            to use in the gradient model
        output_dir: output dirpath to store the results
    """
    # Parse the mapping table file and get the normalized headers and 
    # category translation
    headers, mapping_table_dict = parse_mapping_table(lines)
    # Check that all the mapping files listed in the mapping table exist
    check_exist_filepaths(base_dir, mapping_table_dict.keys())
    # Test the different models
    if 'core' in models:
        core_model_test(mapping_table_dict, output_dir)
    if 'gradient' in models:
        sorted_values = sort
        if sort in ['ascendant', 'descendant']:
            sorted_values = sort_category_values(mapping_table_dict,
                                category, sort)
        gradient_model_test(mapping_table_dict, category, sorted_values,
                            output_dir)
    if 'subpopulation' in models:
        subpopulation_model_test(mapping_table_dict, category, output_dir)