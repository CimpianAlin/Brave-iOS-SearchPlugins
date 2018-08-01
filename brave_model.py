#!/usr/bin/python
#
# Brave model

import json

class BraveModel:
  dictionary = {}

  def __init__(self):
    self.load('brave.json')

  def load(self, name):
    with open(name, 'r') as fp:
      self.dictionary = json.load(fp)
      fp.close()

  def default(self):
    return self.dictionary['default']

  def all_locales(self):
    return self.dictionary['allLocales']

  def search_engines_for_all_locales(self):
    return self.dictionary['allLocales']['visibleDefaultEngines']

  def overrides(self):
    return self.dictionary['overrides']

  def region_overrides(self):
    return self.dictionary['regionOverrides']

  def locales(self):
    return self.dictionary['locales']

  def locale(self, locale):
    return self.dictionary['locales'][locale]

  def key_for_locale(self, locale, key):
    return self.dictionary['locales'][locale][key]

  def search_engines_for_locale(self, locale):
    return self.dictionary['locales'][locale]['default']['visibleDefaultEngines']
