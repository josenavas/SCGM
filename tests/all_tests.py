#!/usr/bin/env python
"""Run all tests.
"""
__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from os import walk
from subprocess import Popen, PIPE, STDOUT
from os.path import join, abspath, dirname
import re

from qiime.util import parse_command_line_parameters

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("", "", "")]
script_info['output_description'] = ""
script_info['required_options'] = []
script_info['optional_options'] = []
script_info['version'] = __version__
script_info['help_on_no_arguments'] = False


def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    test_dir = abspath(dirname(__file__))

    unittest_good_pattern = re.compile('OK\s*$')
    python_name = 'python'
    bad_tests = []

    # Run through all of unit tests, and keep track of any files which
    # fail unit tests.
    unittest_names = []
    for root, dirs, files in walk(test_dir):
        for name in files:
            if name.startswith('test_') and name.endswith('.py'):
                unittest_names.append(join(root, name))

    unittest_names.sort()

    for unittest_name in unittest_names:
        print "Testing %s:\n" % unittest_name
        command = '%s %s -v' % (python_name, unittest_name)
        result = Popen(command, shell=True, universal_newlines=True,
                       stdout=PIPE, stderr=STDOUT).stdout.read()
        print result
        if not unittest_good_pattern.search(result):
                bad_tests.append(unittest_name)

    if bad_tests:
        print "\nFailed the following unit tests.\n%s" % '\n'.join(bad_tests)

if __name__ == "__main__":
    main()
