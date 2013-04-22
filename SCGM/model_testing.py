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
from SCGM.util import check_exist_filepaths, unify_dictionaries, \
                        sort_dictionary_keys, write_similarity_matrix, \
                        write_unused_mapping_files
from SCGM.profile import make_profile_by_sid, make_profiles_by_category, \
                            normalize_profiles, write_profile
from SCGM.stats import bootstrap_profiles, build_similarity_matrix, \
                        is_diagonal_matrix

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
            profiles.append(make_profile_by_sid(mapping_data, sid))
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

def gradient_model_test(profiles, sim_mat, category, sorted_values, output_dir):
    """ Tests the gradient model in the similarity matrix
    Inputs:
        sim_mat: profiles similarity matrix - sorted by sorted_values
        category: category used for generate the similarity matrix
        sorted_values: list of category values sorted
        output_dir: output director
    """
    n = len(sorted_values)
    # First check: sim_mat[0][n-1] == 0
    test_passed = True if sim_mat[0][n-1] == 0 else False
    # Second check: for all i in [0..n-2] sim_mat[i][i+1] > 0
    if test_passed:
        for i in range(n-1):
            if sim_mat[i][i+1] > 0:
                test_passed = False
                break
    # Third check: for all i,j; i < j such that sim_mat[i][j] > 0
    # the amount shared in the result profile from i to j is > 0
    if test_passed:
        # Checking with i == 0 and starting at n-2
        # sim_mat[0][n-1] should be 0 as stated above
        
    # Write the test result
    output_fp = join(output_dir, 'gradient_model_test.txt')
    outf = open(output_fp, 'w')
    outf.write("Gradient model results:\n")
    outf.write("\tCategory used: %s\n" % category)
    outf.write("\tOrder used: %s\n" % ','.join(sorted_values))
    outf.write("\tGradient model test passed: ")
    if test_passed:
        outf.write("Yes\n")
    else:
        outf.write("No\n")
    outf.close()

def subpopulation_model_test(dist_mat, category, output_dir):
    """ Tests the subpopulation model in the profiles distance matrix
    Inputs:
        dist_mat: profiles distance matrix
        category: category used for generate the distance matrix
        output_dir: output directory
    """
    # Write the test result
    output_fp = join(output_dir, 'subpopulation_model_test.txt')
    outf = open(output_fp, 'w')
    outf.write("Subpopulation model results:\n")
    outf.write("\tCategory used: %s\n" % category)
    outf.write("\tSubpopulation model test passed: ")
    # The subpopulation model is followed if the similarity matrix is
    # a diagonal matrix
    if is_diagonal_matrix(dist_mat):
        outf.write("Yes\n")
    else:
        outf.write("No\n")
    outf.close()

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
        # Perform core model testing
        core_model_test(base_dir, mapping_table_dict, output_dir)
    if 'gradient' in models or 'subpopulation' in models:
        # For the gradient and subpopulation models we need to get the 
        # profiles by category value
        profiles = {}
        # Keep track of the mapping files not used in the test
        unused_maps = []
        for mapping_file in mapping_table_dict:
            mapping_fp = join(base_dir, mapping_file)
            mapping_category = mapping_table_dict[mapping_file][category]
            if mapping_category == "No":
                # The mapping file do not have data for this category
                unused_maps.append(mapping_file)
            elif mapping_category == "Yes":
                # 'Yes' its only supported for the category "HEALTHY"
                if category == "HEALTHY":
                    # All the study has been done in healthy people
                    # get the studies by SampleID
                    ret = make_profiles_by_category(mapping_fp, "SampleID")
                    # Get a list of profiles
                    profile_list = [ret[k] for k in ret]
                    # Add the list of profiles of this mapping file to the 
                    # previous profiles
                    if 'healthy' in profiles:
                        profiles['healthy'].extend(profile_list)
                    else:
                        profiles['healthy'] = profile_list
                else:
                    raise ValueError, "The value 'Yes' in the mapping table" + \
                        " it's only supported for the category 'HEALTHY'"
            else:
                # Generate the profiles by category of this mapping file
                map_profiles = make_profiles_by_category(mapping_fp, 
                                mapping_category)
                # Add the profiles of this mapping file to the previous profiles
                profiles = unify_dictionaries(profiles, map_profiles)
        # Get the different values of the category in case that we need to
        # sort them (for the gradient model)
        values = profiles.keys()
        if 'gradient' in models:
            # If we have to test the gradient model, we have to use the values
            # in that category sorted
            if sort in ['ascendant', 'descendant']:
                values = sort_dictionary_keys(profiles,
                                    descendant=(sort=='descendant'))
            else:
                # We use the user defined sort of the values
                values = sort
        # Build similarity matrix from bootstrapped profiles
        sim_mat = build_similarity_matrix(profiles, values)
        # Store the similarity matrix in a file
        sim_mat_fp = join(output_dir, 'similarity_matrix.txt')
        write_similarity_matrix(sim_mat, values, sim_mat_fp)
        # Store in a file the mapping files not used for the similarity matrix
        unused_maps_fp = join(output_dir, 'unused_mapping_files.txt')
        write_unused_mapping_files(unused_maps, unused_maps_fp)
        if 'subpopulation' in models:
            # Perform subpopulation model test
            subpopulation_model_test(sim_mat, category, output_dir)
        if 'gradient' in models:
            # Perform gradient model test
            gradient_model_test(profiles, sim_mat, category, values, output_dir)