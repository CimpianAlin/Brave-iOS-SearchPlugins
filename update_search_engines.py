#!/usr/bin/python
#
# Update Brave search engines with latest changes from Mozilla
# Run ./update_search_engines.py

import os
import argparse

import sys
sys.path.insert(0, 'MozillaOriginals')
import scrape_plugins

from brave_helper import BraveHelper
from mozilla_search_engines import MozillaSearchEngines
from brave_search_engines import BraveSearchEngines
from brave_git import BraveGit

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--scrape', action = 'store_true', help='Scrape Mozilla for latest search engines')
args = parser.parse_args()

mozilla_search_plugins_directory = "MozillaOriginals/SearchPlugins"
brave_overrides_directory = "BraveOverrides"
ios_final_result_directory = "iOSFinalResult"
search_engines_filename = "list.json"

mozilla_search_engines_path = os.path.join(mozilla_search_plugins_directory, search_engines_filename)
brave_search_engines_path = os.path.join(ios_final_result_directory, search_engines_filename)

def copy_files_callback(source, destination):
  print "  Copying file from " + source + " to " + destination

def delete_orphaned_files_callback(filename):
  name, extension = os.path.splitext(filename)
  print "  Deleting orphaned \"" + name + "\" search engine"

brave_helper = BraveHelper()

if args.scrape:
  print "Downloading Mozilla search engines to \"" + mozilla_search_plugins_directory + "\"..."
  scrape_plugins.main()

print "Generating list of Mozilla search engines at \"" + mozilla_search_engines_path + "\"..."
mozilla_search_engines = MozillaSearchEngines()
mozilla_search_engines_dictionary = mozilla_search_engines.generate_list_from_path(mozilla_search_plugins_directory)
brave_helper.save_json(mozilla_search_engines_path, mozilla_search_engines_dictionary, sort_keys = True, indent = 2)

print "Cleaning up \"" + ios_final_result_directory + "\"..."
brave_helper.remove_files_at_path(ios_final_result_directory)

print "Copying Mozilla search engines to \"" + ios_final_result_directory + "\"..."
brave_helper.copy_files(copy_files_callback, mozilla_search_plugins_directory, ios_final_result_directory, ".xml")

print "Copying Brave search engines to \"" + ios_final_result_directory + "\"..."
brave_helper.copy_files(copy_files_callback, brave_overrides_directory, ios_final_result_directory, ".xml")

print "Merging Brave search engines with Mozilla search engines..."
brave_search_engines = BraveSearchEngines()
merged_dictionary = brave_search_engines.merge(mozilla_search_engines_dictionary)

print "Deleting blacklisted search engines..."
brave_search_engines.delete_blacklisted_search_engines(merged_dictionary)
brave_search_engines.delete_globally_blacklisted_search_engines(merged_dictionary)

print "Deleting search engines which already exist in \"all locales\"..."
brave_search_engines.delete_search_engines_which_exist_in_all_locales(merged_dictionary)

print "Overriding Mozilla search engines..."
brave_search_engines.override_search_engines(merged_dictionary)

print "Deleting orphaned search engines at \"" + ios_final_result_directory + "\"..."
search_engines_to_keep = brave_search_engines.search_engines(merged_dictionary)
brave_helper.delete_orphaned_files(delete_orphaned_files_callback, ios_final_result_directory, search_engines_to_keep)

print "Saving Brave search engines to \"" + brave_search_engines_path + "\"..."
brave_helper.save_json(brave_search_engines_path, merged_dictionary, sort_keys = True, indent = 2)

print "Adding untracked changes to the local Git branch..."
brave_git = BraveGit()
brave_git.add_untracked_changes()
brave_git.diff()

print "Committing changes to the local Git branch..."
brave_git.commit("Updated search engines")

print "Pushing changes to the remote Git repository..."
brave_git.push()

print "Successfully updated search engines"
