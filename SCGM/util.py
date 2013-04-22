#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Jose Antonio Navas Molina", "Joshua Shorenstein"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from os.path import exists, join

def check_exist_filepaths(base_dir, mapping_fps):
    """Check that all the mapping files in mapping_fps exist

    Inputs:
        base_dir: the common directory path where all the mapping_fps are 
            relative to
        mapping_fps: a list with the relative filepaths from base_dir to the
            mapping files

    If any of the filepaths does not exists, raises a ValueError
    """
    for fp in mapping_fps:
        fullpath = join(base_dir, fp)
        if not exists(fullpath):
            raise ValueError, "The mapping file %s does not exists" % fullpath

def unify_dictionaries(d1, d2):
    """Inserts the value of the dictionary d2 into d1
    Inputs:
        d1, d2: dictionaries with lists as values
    """
    for k in d2:
        if k in d1:
            d1[k].extend(d2[k])
        else:
            d1[k] = d2[k]
    return d1

def sort_dictionary_keys(d, descendant=False):
    """Sorts the keys of the dictionary d if they are strings encoding numbers
    Inputs:
        d: the dictionary
        descendant: if true it sorts the values in a descendant manner

    Returns a list with sorted keys
    """
    try:
        keys = [float(k) for k in d]
    except:
        raise ValueError, "Automatic values order it's only supported " + \
                                "for numerical categories"
    keys = sorted(keys)
    if descendant:
        keys = keys[::-1]
    keys = [str(k) for k in keys]
    return keys

def format_matrix_position(mat_pos):
    """Gets a string with the value in the matrix position
    Inputs:
        mat_pos: the value in the matrix position
    """
    str_values = map(str, mat_pos)
    return '(' + ','.join(str_values) + ')'

def write_similarity_matrix(sim_mat, header, output_fp):
    """Writes a similarity matrix to a file
    Inputs:
        sim_mat: the similarity matrix
        header: the list of headers of the matrix in the same order as they 
            appear in the similarity matrix
        output_fp: the output filepath
    """
    outf = open(output_fp, 'w')
    outf.write(" \t" + '\t'.join(header) + '\n')
    for i, h in enumerate(header):
        row = map(format_matrix_position, sim_mat[i])
        row.insert(0, h)
        outf.write('\t'.join(row) + '\n')
    outf.close()

def write_unused_mapping_files(maps, output_fp):
    """Writes the list maps to the file output_fp
    Inputs:
        maps: list of unused mapping files
        output_fp: the output filepath
    """
    outf = open(output_fp, 'w')
    outf.write("The following mapping files were not used during the test:\n")
    outf.write("\n".join(maps))
    outf.close()
