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

from SCGM.stats import is_diagonal_matrix


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
