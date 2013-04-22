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
    test_passed = True if sim_mat[0][n-1][0] == 0 else False
    # Second check: for all i in [0..n-2] sim_mat[i][i+1] > 0
    if test_passed:
        for i in range(n-1):
            if sim_mat[i][i+1][0] > 0:
                test_passed = False
                break
    # Third check: for all i,j; i < j such that sim_mat[i][j] > 0
    # the amount shared in the result profile from i to j is > 0
    if test_passed:
        # Checking with i == 0 and starting at n-2
        # sim_mat[0][n-1] should be 0 as stated above
        for j in range(n-1,1,-1):
            if sim_mat[0][j][0] > 0:
                # value 0 and j share something - test that the result
                # profile of comparing all the profiles in the categories from
                # 0 to j share something
                # profs = profiles[sorted_values[0]]
                # for i in range()
                # prof, shared, std, ci = bootstrap_profiles(profs)
                # if latest_j_tested < j:
                #     latest_j_tested
                raise ValueError, "This test is broken... fix it!!!"
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