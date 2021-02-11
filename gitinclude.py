#!/usr/bin/env python
'''
A command line application for constructing a .gitignore file
from a collection of directory, [file/filteype] pairs.
'''

import os
from collections import OrderedDict

def path_dict_to_ordered_dict(path_dict):
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
        print(relative_path)

        for i in (i for i, l in enumerate(relative_path[:-1])
                  if l == os.path.sep):
            subpath = relative_path[:i+1]
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


if __name__ == '__main__':
    d = {"/test/test1/test2/": ["*.txt", "*.cpp"],
         "/test/": ["*.txt"],
         "/": ["*.cpp"]}
    od = path_dict_to_ordered_dict(d)
    print("\n".join(generate(od)))
