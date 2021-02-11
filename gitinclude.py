#!/usr/bin/env python
'''
A command line application for constructing a .gitignore file
from a collection of directory, [file/filteype] pairs.
'''

import sys
import os
from collections import OrderedDict


def order_path_dict(path_dict):
    '''Return an ordered dictionary with all the subpaths from path_dict

    Arguments
    ---------
    path_dict : {relative_path: [*.py, *.cpp, ...]}

    Returns
    -------
    A list of strings describing the gitignore.
    '''
    ordered_dict = OrderedDict()
    for relative_path, extensions in path_dict.items():
        for i in (i for i, l in enumerate(relative_path[:-1])
                  if l == os.path.sep):
            subpath = relative_path[:i + 1]
            if subpath not in ordered_dict:
                ordered_dict[subpath] = None

        ordered_dict[relative_path] = extensions

    return ordered_dict


def generate(ordered_path_dict):
    '''Return a list of gitignore lines as specified by the ordered dictionary.

    Arguments
    ---------
    ordered_path_dict : OrderedDict("relative_path": [*.py, *.cpp, ...])

    Returns
    -------
    A list of .gitignore lines
    '''
    result = ["*"]
    for path, extensions in ordered_path_dict.items():
        if path != "/":
            result.append("!" + path)
            result.append(path + "*")

        for ext in (extensions or []):
            result.append("!" + path + ext)

    return result


def parse_file(filename):
    '''Parse a gitinclude file and return a dictionary.'''
    path_dict = dict()
    with open(filename, 'r') as gitinclude_file:
        for line in filter(None, (''.join(line.split())
                                  for line in gitinclude_file)):
            target_dir, extensions = line.rsplit("[", 1)
            extensions = extensions[:-1].split(',')
            path_dict[target_dir] = extensions

    return path_dict


def write_to_gitignore(rules, target=".gitignore"):
    '''Write rules to .gitignore file.'''
    with open(target, 'w') as gitignore_file:
        gitignore_file.writelines("{}\n".format(rule) for rule in rules)


def gitinclude(filename, target=".gitignore"):
    '''Generate rules from gitinclude file.'''
    rules = generate(order_path_dict(parse_file(filename)))
    write_to_gitignore(rules, target)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Please specify a gitinclude file")
    elif len(sys.argv) == 2:
        gitinclude(sys.argv[1])
    elif len(sys.argv) == 3:
        gitinclude(sys.argv[1], sys.argv[2])
    else:
        print("Too many command line arguments")
