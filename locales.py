#!/usr/bin/python
#
# Get list of locales from a specified path

import os

from brave_helper import BraveHelper

class Locales:
  brave_helper = BraveHelper()

  def from_path(self, path):
    locales = []

    for dir in os.listdir(path):
      if os.path.isdir(os.path.join(path, dir)):
        if self.brave_helper.should_skip_path(path):
          continue

        locale = self.brave_helper.parent_directory(dir)
        locales.append(locale)

    return locales
