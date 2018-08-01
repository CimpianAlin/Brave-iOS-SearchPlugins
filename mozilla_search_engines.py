#!/usr/bin/python
#
# Generate Mozilla earch engines

import os

from locales import Locales

class MozillaSearchEngines:
  locales = Locales()

  def for_locale_from_path(self, locale_path):
    search_engines = []

    file_path = os.path.join(locale_path, "list.txt")
    with open(file_path, "r") as file:
      search_engines = file.read().splitlines()
      file.close()

    return search_engines

  def for_all_locales_from_path(self, path):
    dictionary = {}

    locales = self.locales.from_path(path)
    for locale in sorted(locales):
      print "Processing \"" + locale + "\" locale"

      locale_path = os.path.join(path, locale)
      search_engines = self.for_locale_from_path(locale_path)
      for search_engine in search_engines:
        print "  Adding \"" + search_engine + "\" search engine"

      dictionary[locale] = {'default': {'visibleDefaultEngines': search_engines}}

    return dictionary

  def append_search_engines_from_path(self, path, dictionary):
    search_engines = self.for_all_locales_from_path(path)
    dictionary['locales'] = search_engines

  def generate_list_from_path(self, path):
    dictionary = {}
    self.append_search_engines_from_path(path, dictionary)

    return dictionary
