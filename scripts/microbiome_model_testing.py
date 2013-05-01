#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from qiime.util import parse_command_line_parameters, make_option
from SCGM.model_testing import microbiome_model_test, VALID_MODELS
from os import mkdir
from os.path import exists

script_info = {}
script_info['brief_description'] = """Tests the microbiome models presented in\
 Hamady and Knight, Genome research, vol. 19, no. 7, pp. 1141-52 Jul. 2009."""
script_info['script_description'] = """This script takes the mapping files\
 generated in the QIIME's script summarize_taxa.py and tests the microbiome\
 models presented in Hamady and Knight, Genome research, vol. 19, no. 7, pp.\
 1141-52 Jul. 2009.

 It uses the overlapping metric described in the course project proposal to\
 test the different models.

 The mapping table is a tab delimited file where columns are categories\
 (metadata) and rows are mapping files. The headers line should start with a #\
 symbol and the first headers should be 'mapping_fp'. This column will contain\
 the relative path to the mapping file from the 'input_dir' folder. The other\
 headers in the mapping table should be category fields that the user may be\
 interested to test the subpopulation and gradient models. Then, the position\
 i, j of the table will hold the header j for the mapping file i. This\
 conversion is needed because the mapping files can be from different studies\
 and the header can be different although they have the same meaning. Thus,\
 this file can normalize all the metadata headers.
 """
script_info['script_usage'] = [
    ("Example:", "Test all the models against all the mapping files listed in "+
        "'map_table.txt' and use the 'Treatment' category for the gradient and"+
        " subpopulation model, using the order 'control,treatment_1,"+
        "treatment_2' for the gradient model. The common base folder for all" +
        " the mapping files is 'base_dir' and it stores the output in the " + 
        "'output' folder",
        "%prog -i base_dir -m map_table.txt -o output -c Treatment " +
            "-s control,treatment_1,treatment_2"),

    ("Example:", "Test only the core model",
        "%prog -i base_dir -m map_table.txt -o output -t core"),

    ("Example:", "Test only the subpopulation model",
        "%prog -i base_dir -m map_table.txt -o output -t subpopulation " +
            "-c Geography"),

    ("Example:", "Test only the gradient model, leaving the code to " + 
        "automatically order the values in an ascendant order",
        "%prog -i base_dir -m map_table.txt -o output -t gradient " +
            "-c Age -s ascendant")]
script_info['output_description'] = """The output is a plain text file\
 indicating the models supported by the data. Further files are generated\
 depending on the model tested:
    - Core: a tab delimited file containing the result profile.
    - Subpopulation: a tab delimited file containing the result profile for\
 each value in the category.
    - Gradient: a tab delimited file containing the result profile for each\
 value in the category.
"""
script_info['required_options'] = [
    make_option('-i', '--input_dir', type='existing_dirpath',
        help="Base directory where the mapping files listed in the mapping " + 
            "table are located"),
    make_option('-m', '--mapping_table_fp', type='existing_filepath',
        help="The path to the mapping table file."),
    make_option('-l', '--level', type='int',
        help="The taxa level."),
    make_option('-o', '--output_dir', type='new_dirpath',
        help="Path to the output directory.")
]
script_info['optional_options'] = [
    make_option('-t', '--models_to_test', type='multiple_choice',
        mchoices=VALID_MODELS, default=VALID_MODELS,
        help="Comma separated list of microbiome models to test. Valid " +
            "options are: %s"  % VALID_MODELS + " [default: %default]"),
    make_option('-c', '--category', type='string', default=None,
        help="In case of testing the 'gradient' or 'subpopulation' models, " + 
            "the category in the mapping table to be used."),
    make_option('-s', '--sort', type='string', default=None,
        help="In case of testing the 'gradient' model, an ordered comma " +
            "separated list with the values of the given category in the order"+
            " that should be tested. If using a numerical value, you can use " +
            "'ascendant' or 'descendant' to sort the values ascendant or " +
            "descendant, respectively."),
    make_option('--min_samples', type='int', default=None,
        help="In case of testing the 'gradient' or 'subpopulation' models " +
            "the number of samples to include in each category. If the " +
            "category has less samples than specified, the category is not " +
            "included in the test. If you don't provide any value, no " +
            "subsampling will be performed. If the value is 0, the " + 
            "subsampling depth will default to the minimum number of samples " +
            "needed to include all the categories. [default: %default]"),
    make_option('-n', '--num_subsamples', type='int', default=100,
        help="In case of doing subsampling, the number of times the data is " +
            "subsample before creating the consensus matrix. " +
            "[default: %default]")
]
script_info['version'] = __version__

if __name__ == '__main__':
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    # Perform needed parameter checking:
    # If we had to test the subpopulation model, we need a category
    if 'subpopulation' in opts.models_to_test and not opts.category:
        raise ValueError, "A category should be passed in order to test " +\
            "the subpopulation model."
    # If we had to test the gradient model, we need a category and a list of
    # sorted values in this category
    if 'gradient' in opts.models_to_test:
        if not opts.category:
            raise ValueError, "A category should be passed in order to test " +\
                "the gradient model."
        if not opts.sort:
            raise ValueError, "An order for the category should be passed " + \
                "in order to test the gradient model."

    # Get the parameters
    input_dir = opts.input_dir
    map_table_fp = opts.mapping_table_fp
    model = opts.models_to_test
    output_dir = opts.output_dir
    category = opts.category
    sort = opts.sort
    subsampling_depth = opts.min_samples
    num_subsamples = opts.num_subsamples

    if subsampling_depth:
        if subsampling_depth < 0:
            raise ValueError, "The number of minimum samples to keep should" + \
                " greater or equal to 0."

    if num_subsamples < 1:
        raise ValueError, "The number of subsamples has to be greater or " + \
            "equal to 1."


    # Try to create the output folder
    if not exists(output_dir):
        mkdir(output_dir)

    # Open the mapping table file
    map_table = open(map_table_fp, 'U')

    # Test the models
    microbiome_model_test(input_dir, map_table, model, opts.level, category,
        sort, subsampling_depth, num_subsamples, output_dir)

    # Close the mapping table file
    map_table.close()