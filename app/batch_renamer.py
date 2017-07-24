#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import argparse


def match_keyword(old_pattern, new_pattern, root_path):
    """ Create lists for matched files and dirs

    Returns: list of matched files, list of dirs to be renamed

    """
    file_list = []
    dir_list = []

    regex = re.compile(r'.*([^a-zA-Z]|\b)%s([^a-zA-Z]|\b).*' %
                       re.escape(old_pattern))

    for root, dirs, files in os.walk(root_path):

        for file in files:

            if regex.match(file):
                file_list.append(root + '/' + file)

        # directories have to be added to the list after all files
        # contained inside
        if regex.match(os.path.basename(root)):
            print("\nFound directory.")
            print(root)
            confirm = input(" Rename? (y/N): ")

            if confirm == 'y':
                dir_list.append(root)

    return file_list, dir_list


def revreplace(string, old, new, occurrence):
    # Replace from last to first
    tmp = string.rsplit(old, occurrence)
    return new.join(tmp)


def rename_items(item_list, old_pattern, new_pattern):
    """ Rename every single item in given list.

    Returns: List of renamed items
    """
    modified_list = []
    for item in item_list:
        # Replace only last occurrence in string (which is the file name)
        renamed_item = revreplace(item, old_pattern, new_pattern, 1)
        modified_list.append(renamed_item)
        print_items_to_be_renamed(item, renamed_item)
        os.rename(item, renamed_item)

    return modified_list


def print_items_to_be_renamed(item, ren_item):
    # Print old and new file name
    print("\nFrom: " + item)
    print("To:  " + ren_item + "\n")


def print_match_list(file_list, path):
    # Print the whole list of matched files for revision
    print()
    for item in file_list:
        print(item.lstrip(path))
    print()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Replace file names under given path recursively')

    # Add command line arguments, only the path is obligatory
    parser.add_argument('-k', '--keyword',
                        help='String to be replaced')
    parser.add_argument('-r', '--replacement',
                        help='String replacing keyword')
    parser.add_argument('-p', '--path',
                        help='Path to be searched', required=True)
    args = vars(parser.parse_args())

    # If keyword is not given as argument ask for it
    if args['keyword']:
        keyword = args['keyword']
    else:
        keyword = input("Keyword: ")

    # If keyword replacement is not given as argument ask for it
    if args['replacement']:
        keyword_replace = args['replacement']
    else:
        keyword_replace = input("Keyword Replacement: ")

    if args['path']:
        path = args['path']

    # Make sure we don't end up with duplicated slashes
    path = path.rstrip('/')

    # Get both lists
    files, dirs = match_keyword(keyword, keyword_replace, path)

    # We need to rename files first, so the path doesn't get messed up
    if files:
        print_match_list(files, path)

        answer = input("Change all? (y/N): ")

        if answer is 'y':
            list_renamed = rename_items(files, keyword, keyword_replace)

    # Lastly, the directories can be renamed
    if dirs:
        list_renamed_dirs = rename_items(dirs, keyword, keyword_replace)
        print("Directories Renamed: ", list_renamed_dirs)
