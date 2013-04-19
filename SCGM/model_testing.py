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

from os.path import join
from qiime.parse import parse_mapping_file_to_dict

from SCGM.parse import parse_mapping_table
from SCGM.util import check_exist_filepaths, sort_category_values
from SCGM.profile import make_profile, compare_profiles, normalize_profiles, \
                            write_profile
from SCGM.stats import bootstrap_profiles

def core_model_test(base_dir, mapping_table, output_dir):
    """ Tests the core model
    Inputs:
        base_dir: base common directory of all mapping files
        mapping_table: dictionary with the mapping table information
        output_dir: output directory
    """
    profiles = []
    # Loop through all the mapping files
    for map_file in mapping_table:
        # Get the path to the mapping file
        map_fp = join(base_dir, map_file)
        # Parse the mapping file in a dictionary
        map_f = open(map_fp, 'U')
        mapping_data, comments = parse_mapping_file_to_dict(map_f)
        map_f.close()
        # Create a profile for each sample in this mapping file
        for sid in mapping_data:
            profiles.append(make_profile(mapping_data, [sid]))
    # Bootstrap profiles to get the results
    profile, mean, stdev, ci = bootstrap_profiles(normalize_profiles(profiles))
    # Write the bootstrapped profile
    profile_fp = join(output_dir, 'core_model_profile.txt')
    write_profile(profile, profile_fp, bootstrapped=True)
    # Write the test result
    output_fp = join(output_dir, 'core_model_result.txt')
    outf = open(output_fp, 'w')
    outf.write("Results for the core model test:\n")
    outf.write("Microbiome model: ")
    if profile['not_shared'][0] < 0.5:
        outf.write("Substantial core.\n")
    elif profile['not_shared'][0] < 1.0:
        outf.write("Minimal core.\n")
    else:
        outf.write('No core\n')
    outf.write("\nStatistical results (amount shared):\n")
    outf.write("Mean: %f %%\n" % (mean * 100))
    outf.write("Standard deviation: %f %%\n" % (stdev * 100))
    outf.write("Confidence interval for the mean: [%f %%, %f %%]\n"
                 % ((ci[0] * 100), (ci[1] * 100)))

def gradient_model_test(mapping_table, category, sorted_values, output_dir):
    raise ValueError, "Function not implemented"

def subpopulation_model_test(mapping_table, category, output_dir):
    raise ValueError, "Function not implemented"

def microbiome_model_test(base_dir, lines, models, category, sort, output_dir):
    """ Tests the microbiome models listed in 'models'

    Inputs:
        base_dir: base common directory of all mapping files
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
        core_model_test(base_dir, mapping_table_dict, output_dir)
    if 'gradient' in models:
        sorted_values = sort
        if sort in ['ascendant', 'descendant']:
            sorted_values = sort_category_values(mapping_table_dict,
                                category, sort)
        gradient_model_test(mapping_table_dict, category, sorted_values,
                            output_dir)
    if 'subpopulation' in models:
        subpopulation_model_test(mapping_table_dict, category, output_dir)