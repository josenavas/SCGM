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

from os.path import join, exists
from os import mkdir

from SCGM.parse import parse_mapping_table
from SCGM.util import (check_exist_filepaths, unify_dictionaries,
                       sort_dictionary_keys, write_similarity_matrix,
                       write_unused_mapping_files)
from SCGM.profile import (make_profiles_by_category, write_profile,
                          build_consensus_profiles, subsample_profiles)
from SCGM.stats import build_similarity_matrix, build_consensus_matrix
from SCGM.core_model_test import core_model_test
from SCGM.subpopulation_model_test import subpopulation_model_test
from SCGM.gradient_model_test import gradient_model_test


def microbiome_model_test(base_dir, lines, models, taxa_level, category, sort,
                          subsampling_depth, num_subsamples, output_dir):
    """ Tests the microbiome models listed in 'models'

    Inputs:
        base_dir: base common directory of all mapping files
        lines: mapping table file lines
        models: list of models to test
        category: category to use in the gradient or subpopulation models
        sort: list of category values sorted, or 'ascendant' or 'descendant'
            to use in the gradient model
        subsampling_depth: number of sequences to keep in each subsample
        num_subsamples: number of subsamples
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
        core_model_test(base_dir, mapping_table_dict, taxa_level, output_dir)
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
                    ret = make_profiles_by_category(mapping_fp, taxa_level,
                                                    "SampleID")
                    # Get a list of profiles
                    profile_list = [ret[k][0] for k in ret]
                    # Add the list of profiles of this mapping file to the
                    # previous profiles
                    if 'healthy' in profiles:
                        profiles['healthy'].extend(profile_list)
                    else:
                        profiles['healthy'] = profile_list
                else:
                    raise ValueError("""The value 'Yes' in the mapping table
                                     is only supported for the category
                                     'HEALTHY'""")
            else:
                # Generate the profiles by category of this mapping file
                map_profiles = make_profiles_by_category(mapping_fp,
                                                         taxa_level,
                                                         mapping_category)
                # Add the profiles of this mapping file to the previous
                profiles = unify_dictionaries(profiles, map_profiles)
        # Get the different values of the category in case that we need to
        # sort them (for the gradient model)
        values = profiles.keys()
        if 'gradient' in models:
            # If we have to test the gradient model, we have to use the values
            # in that category sorted
            if sort in ['ascendant', 'descendant']:
                # We remove any None value in order to properly order
                profiles.pop("None")
                values = sort_dictionary_keys(profiles,
                                              descendant=(sort == 'descendant'))
            else:
                # We use the user defined sort of the values
                sort = sort.split(',')
                if len(values) != len(sort):
                    raise ValueError("""The number of values in the sorted
                        list and the number of values found in the mapping
                        file are not the same.""")
                values = sort
        # Create a folder to store the subsampled similarity matrices
        sim_mat_folder = join(output_dir, 'subsampled_matrices')
        if not exists(sim_mat_folder):
            mkdir(sim_mat_folder)
        # Initialize matrix list and profiles list
        matrix_list = []
        profiles_list = []
        for i in range(num_subsamples):
            # Subsample the profiles
            subsampled_profiles = subsample_profiles(profiles,
                                                     subsampling_depth, values)
            # Build similarity matrix from bootstrapped profiles
            sim_mat, group_profiles = build_similarity_matrix(
                subsampled_profiles, values)
            matrix_list.append(sim_mat)
            profiles_list.append(group_profiles)
            # Store the similarity matrix in a file
            sim_mat_fp = join(sim_mat_folder, 'similarity_matrix_%d.txt' % i)
            write_similarity_matrix(sim_mat, values, sim_mat_fp)
        # Build consensus matrix
        consensus_mat = build_consensus_matrix(matrix_list)
        # Store the consensus matrix in a file
        cons_mat_fp = join(output_dir, 'consensus_matrix.txt')
        write_similarity_matrix(consensus_mat, values, cons_mat_fp)
        # Build consensus profiles
        consensus_profiles = build_consensus_profiles(profiles_list)
        # Store the profile of each group
        for key in consensus_profiles:
            prof_fp = join(output_dir, str(key + '_consensus_profile.txt'))
            write_profile(consensus_profiles[key], prof_fp, consensus=True)
        # Store in a file the mapping files not used for the similarity matrix
        unused_maps_fp = join(output_dir, 'unused_mapping_files.txt')
        write_unused_mapping_files(unused_maps, unused_maps_fp)
        if 'subpopulation' in models:
            # Perform subpopulation model test
            subpopulation_model_test(consensus_mat, category, output_dir)
        if 'gradient' in models:
            # Perform gradient model test
            gradient_model_test(consensus_profiles, consensus_mat, category,
                                values, output_dir)
