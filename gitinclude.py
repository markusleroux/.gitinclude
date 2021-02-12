#!/usr/bin/env python
'''
A command line application for constructing a .gitignore file
from a collection of directory, [file/filteype] pairs.
'''

import sys
import os
from collections import OrderedDict

Docstring = ["#---------------------------------------------------------#",
             "# **********************.gitinclude********************** #",
             "#---------------------------------------------------------#",
             "# This gitignore files was generated using the gitinclude #",
             "# command line application from a set of rules regarding  #",
             "# which files should be kept.                             #",
             "#                                                         #",
             "#      https://github.com/markusleroux/.gitinclude.git    #",
             "#---------------------------------------------------------#\n"]

def generate(ordered_path_dict):
    '''Return a list of gitignore lines as specified by the ordered dictionary.

    Arguments
    ---------
    ordered_path_dict : OrderedDict("relative_path": [*.py, *.cpp, ...])

    Returns
    -------
    A list of .gitignore lines
    '''
    result = Docstring
    result.append("\n\n# Ignore all:\n# ---------------------------\n*")

    for path, extensions in ordered_path_dict.items():
        result.append("\n\n# Directory: {} \n# Rules: {}".format(path, extensions))
        result.append("# ---------------------------")
        if path != "/":
            result.append("!" + path)
            result.append(path + "*")

        for ext in (extensions or []):
            result.append("!" + path + ext)

    return result


def parse_file(filename):
    '''Parse a gitinclude file and return an ordered dictionary.'''
    ordered_dict = OrderedDict()
    with open(filename, 'r') as gitinclude_file:
        for line in filter(None, (''.join(line.split())
                                  for line in gitinclude_file)):
            target_dir, extensions = line.rsplit("[", 1)
            extensions = extensions[:-1].split(',')

            for i in (i for i, l in enumerate(target_dir[:-1]) if l == os.path.sep):
                subpath = target_dir[:i+1]
                if subpath not in ordered_dict:
                    ordered_dict[subpath] = None

            ordered_dict[target_dir] = extensions

    return ordered_dict


def write_to_gitignore(rules, target=".gitignore"):
    '''Write rules to .gitignore file.'''
    with open(target, 'w') as gitignore_file:
        gitignore_file.writelines("{}\n".format(rule) for rule in rules)


def gitinclude(filename, target=".gitignore"):
    '''Generate rules from gitinclude file.'''
    rules = generate(parse_file(filename))
    write_to_gitignore(rules, target)
    print("{} written".format(target))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Please specify a gitinclude file")
    elif len(sys.argv) == 2:
        gitinclude(sys.argv[1])
    elif len(sys.argv) == 3:
        gitinclude(sys.argv[1], sys.argv[2])
    else:
        print("Too many command line arguments")
