#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import argparse


def match_keyword(old_pattern, new_pattern, root_path):
    """ Returns: file list of matched items
        Create file list of matched items
    """
    file_list = []
    dir_list = []

    regex = re.compile(r'.*([^a-zA-Z]|\b)%s([^a-zA-Z]|\b).*' %
                       re.escape(old_pattern))

    for root, dirs, files in os.walk(root_path):
        # print("Debugging")
        # print("root", root)
        # print("dirs: ", str(dirs))
        # print("files: ", files)

        for file in files:

            if regex.match(file):
                file_list.append(root + '/' + file)

        if regex.match(os.path.basename(root)):
            # file_list.append(root)
            print("\nFound directory.")
            print(root)
            confirm = input(" Rename? (y/N): ")

            if confirm == 'y':
                dir_list.append(root)

    return file_list, dir_list


def revreplace(string, old, new, occurrence):
    li = string.rsplit(old, occurrence)
    return new.join(li)


def rename_items(item_list, old_pattern, new_pattern):
    """ Returns: List of renamed items
        Rename every single item in given list
    """
    modified_list = []
    for item in item_list:
        renamed_item = revreplace(item, old_pattern, new_pattern, 1)
        modified_list.append(renamed_item)
        print_items_to_be_renamed(item, renamed_item)
        os.rename(item, renamed_item)

    return modified_list


def print_items_to_be_renamed(item, ren_item):
    print("\nFrom: " + item)
    print("To:  " + ren_item + "\n")


def print_match_list(file_list, path):
    print()
    for item in file_list:
        print(item.lstrip(path))
    print()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Replace file names under given path recursively')

    parser.add_argument('-k', '--keyword',
                        help='String to be replaced')
    parser.add_argument('-r', '--replacement',
                        help='String replacing keyword')
    parser.add_argument('-p', '--path',
                        help='Path to be searched', required=True)
    args = vars(parser.parse_args())

    if args['keyword']:
        keyword = args['keyword']
    else:
        keyword = input("Keyword: ")
    if args['replacement']:
        keyword_replace = args['replacement']
    else:
        keyword_replace = input("Keyword Replacement: ")

    if args['path']:
        path = args['path']

    # Make sure we don't end up with duplicated slashes
    path = path.rstrip('/')

    files, dirs = match_keyword(keyword, keyword_replace, path)

    if files:
        print_match_list(files, path)

        answer = input("Change all? (y/N): ")

        if answer is 'y':
            list_renamed = rename_items(files, keyword, keyword_replace)

    if dirs:
        list_renamed_dirs = rename_items(dirs, keyword, keyword_replace)
        print("Directories Renamed: ", list_renamed_dirs)
