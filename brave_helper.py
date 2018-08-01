#!/usr/bin/python
#
# Brave helper

import os
import shutil
import json

class BraveHelper:
  blacklisted_parent_directories = []

  def parent_directory(self, path):
    norm_path = os.path.normpath(path)
    path_components = norm_path.split(os.sep)
    directory = path_components[0]
    return directory

  def should_skip_path(self, path):
    directory = self.parent_directory(path)
    if directory in self.blacklisted_parent_directories:
      return True

    return False

  def remove_files_at_path(self, path):
    if os.path.exists(path):
      shutil.rmtree(path)
    os.mkdir(path)

  def copy_files(self, callback, source_path, destination_path, *extensions):
    for path, directories, files in os.walk(source_path):
      if self.should_skip_path(path):
        continue

      for file in files:
        name, extension = os.path.splitext(file)
        if not extension in extensions:
          continue

        source = os.path.join(path, file)
        destination = os.path.join(destination_path, file)

        if callback:
          callback(source, destination)

        shutil.copy(source, destination)

  def delete_orphaned_files(self, callback, source_path, files_to_keep):
    for path, directories, files in os.walk(source_path):
      for file in files:
        if file in files_to_keep:
          continue

        if callback:
          callback(file)

        file_path = os.path.join(path, file)
        os.remove(file_path)

  def save_json(self, name, object, sort_keys = True, indent = 2, ensure_ascii = True):
    with open(name, 'w') as fp:
      json.dump(object, fp, sort_keys = sort_keys, indent = indent, ensure_ascii = ensure_ascii)
      fp.close()
