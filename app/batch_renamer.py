#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re

usage_msg = """

USAGE: batch_renamer PATTERN_OLD PATTERN_NEW PATH

PATTERN_OLD: The pattern you are searching for and want to change
PATTERN_NEW: The pattern with which the old pattern will be replaced
PATH:        Path which will be searched
"""


class ArgumentException(Exception):
    """Exception raised when wrong number of arguments is given"""
    def __init__(self, msg=None):
        if msg is None:
            # Default  error message
            msg = usage_msg
        super().__init__(msg)
        self.msg = msg


def match_keyword(kw, kwr, root_path):
    """ Returns: file list of matched items
        Create file list of matched items
    """
    file_list = []

    regex = re.compile(r'.*([^a-zA-Z]|\b)%s[^a-zA-Z].*' % re.escape(kw))

    for root, dirs, files in os.walk(root_path):

        if regex.match(root):
            file_list.append(root)

        for file in files:

            if regex.match(file):
                file_list.append(root + '/' + file)

    return file_list


def rename_items(item_list, old_pattern, new_pattern):
    """ Returns: List of renamed items
        Rename every single item in given list
    """
    modified_list = []
    for item in item_list:
        renamed_item = re.sub(re.escape(old_pattern), new_pattern, item)
        modified_list.append(renamed_item)
        print_items_to_be_renamed(item, renamed_item)
        os.rename(item, renamed_item)

    return modified_list


def print_items_to_be_renamed(item, ren_item):
        print()
        print(item)
        print("TO:")
        print(ren_item)
        print()


def print_match_list(l):
    print()
    for item in l:
        print(os.path.basename(item))
    print()


if __name__ == "__main__":

    num_args = len(sys.argv)

    if num_args != 4:
        raise ArgumentException
        sys.exit()


keyword = sys.argv[1]
keyword_replace = sys.argv[2]
path = sys.argv[3]

fl = match_keyword(keyword, keyword_replace, path)

print_match_list(fl)

answer = input("Change all? (y/N)")

if answer is 'y':
    try:
        list_renamed = rename_items(fl, keyword, keyword_replace)
    except FileNotFoundError:
        # Found a directory. The path names changed, so we need to
        # regenerate the list
            fl = match_keyword(keyword, keyword_replace, path)
            list_renamed = rename_items(fl, keyword, keyword_replace)
