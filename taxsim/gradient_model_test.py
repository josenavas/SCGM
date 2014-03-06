#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from os.path import join
from SCGM.profiles import compare_profiles
from SCGM.stats import bootstrap_profiles


def gradient_subarray_check(cons_profs, sim_mat, sorted_values, i, j):
    """Checks if the gradient models holds between values i and j"""
    profs = []
    for k in range(i, j+1):
        profs.extend(cons_profs[sorted_values[k]])
        p = compare_profiles(profs, consensus=True)
        if p['not_shared'] > 0.9999999:
            return False
    return True


def gradient_model_checks(cons_profs, sim_mat, sorted_values, n):
    """Checks if the similarity matrix models a gradient
    """
    # First check: sim_mat[0][n-1] == 0
    if sim_mat[0][n-1][0] > 0:
        return False
    # Second check: for all i in [0..n-2] sim_mat[i][i+1] > 0
    for i in range(n-1):
        if sim_mat[i][i+1][0] == 0:
            return False
    # Third check: for all i,j; i < j such that sim_mat[i][j] > 0
    # all the values between i and j follows a gradient subarray
    # We check i == 0 outside the loop
    for j in range(n-2, 1, -1):
        if sim_mat[0][j][0] > 0:
            if not gradient_subarray_check(cons_profs, sim_mat, sorted_values,
                                           0, j):
                return False
            # If it holds for the largest j, it holds for smaller j
            break
    # Check i > 0
    for i in range(1, n):
        for j in range(n-1, i, -1):
            if sim_mat[i][j][0] > 0:
                if not gradient_subarray_check(cons_profs, sim_mat,
                                               sorted_values, i, j):
                    return False
                break
    # All the checks passed, return True
    return True


def gradient_model_test(cons_profs, sim_mat, category, sorted_values, out_dir):
    """ Tests the gradient model in the similarity matrix
    Inputs:
        cons_profs: consensus profiles by group
        sim_mat: profiles similarity matrix - sorted by sorted_values
        category: category used for generate the similarity matrix
        sorted_values: list of category values sorted
        out_dir: output director
    """
    # Write the test result
    output_fp = join(out_dir, 'gradient_model_test.txt')
    outf = open(output_fp, 'w')
    outf.write("Gradient model results:\n")
    outf.write("\tCategory used: %s\n" % category)
    outf.write("\tOrder used: %s\n" % ','.join(sorted_values))
    outf.write("\tGradient model test passed: ")
    if gradient_model_checks(cons_profs, sim_mat, sorted_values,
                             len(sorted_values)):
        outf.write("Yes\n")
    else:
        outf.write("No\n")
    outf.close()
