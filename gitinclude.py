#!/usr/bin/env python

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
        # print(relative_path)
        relative_path = os.path.normpath(relative_path)
        # print(relative_path)

        for i in (i for i, l in enumerate(relative_path)
                  if l == os.path.sep):
            subpath = relative_path[:i+1]
            if subpath not in ordered_dict:
                ordered_dict[subpath] = None

        ordered_dict[relative_path + os.path.sep] = extensions

    # print("\n\n")
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
        result.append("!" + os.path.sep + path)
        result.append(os.path.sep + path + "*")
        for ext in (extensions or []):
            result.append("!" + os.path.sep + path + ext)

    return result


if __name__ == '__main__':
    d = {"test/test1/test2/": ["*.txt", "*.cpp"],
         "test/": ["*.txt"]}
    od = path_dict_to_ordered_dict(d)
    print("\n".join(generate(od)))
