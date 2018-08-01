#!/usr/bin/python
#
# Generate Brave search engines

from brave_model import BraveModel

class BraveSearchEngines:
  brave_model = BraveModel()

  def merge(self, dictionary):
    dictionary['default'] = self.brave_model.default()
    dictionary['allLocales'] = self.brave_model.all_locales()
    dictionary['regionOverrides'] = self.brave_model.region_overrides()

    brave_locales = self.brave_model.locales()
    locales = dictionary['locales']

    for locale in sorted(brave_locales):
      print "Processing \"" + locale + "\" locale..."

      if locale in locales:
        keys = self.brave_model.locale(locale)
        for key in keys:
          if key == "blacklistedEngines":
            continue
          elif key == "default":
            brave_search_engines = self.brave_model.search_engines_for_locale(locale)
            search_engines = dictionary['locales'][locale]['default']['visibleDefaultEngines']

            merged = False
            for search_engine in brave_search_engines:
              if search_engine in search_engines:
                 print "  Skipping \"" + search_engine + "\" search engine as already exists"
              else:
                 print "  Merging \"" + search_engine + "\" search engine"
                 search_engines.append(search_engine)
                 merged = True

            if merged:
              dictionary['locales'][locale]['default']['visibleDefaultEngines'] = search_engines
          else:
            print "  Merging \"" + key + "\" key from Brave"
            dictionary['locales'][locale][key] = self.brave_model.key_for_locale(locale, key)
      else:
        print "  Merging \"" + locale + "\" locale from Brave"
        dictionary['locales'][locale] = self.brave_model.locale(locale)

    return dictionary

  def delete_search_engine_for_locale(self, dictionary, search_engine, locale):
    if search_engine in dictionary['locales'][locale]['default']['visibleDefaultEngines']:
      print "  Deleting \"" + search_engine + "\" search engine from \"" + locale + "\" locale"
      dictionary['locales'][locale]['default']['visibleDefaultEngines'].remove(search_engine)

  def delete_blacklisted_search_engines(self, dictionary):
    locales = self.brave_model.locales()

    for locale in sorted(locales):
      if locale in dictionary['locales']:
        search_engines_to_remove = []

        if 'blacklistedEngines' in self.brave_model.locale(locale):
          search_engines_to_remove = self.brave_model.locale(locale)['blacklistedEngines']

        if 'blacklistedEngines' in dictionary['locales'][locale]:
          del dictionary['locales'][locale]['blacklistedEngines']

        for search_engine_to_remove in search_engines_to_remove:
          self.delete_search_engine_for_locale(dictionary, search_engine_to_remove, locale)

  def delete_globally_blacklisted_search_engines_recursively(self, dictionary, blacklisted_search_engines):
    for key, value in dictionary.items():
      if isinstance(value, dict):
        self.delete_globally_blacklisted_search_engines_recursively(value, blacklisted_search_engines)
      else:
        if key == "visibleDefaultEngines":
          search_engines = value
          for blacklisted_search_engine in blacklisted_search_engines:
            if blacklisted_search_engine in search_engines:
              search_engines.remove(blacklisted_search_engine)
          dictionary[key] = search_engines

  def delete_globally_blacklisted_search_engines(self, dictionary):
    all_locales = self.brave_model.all_locales()
    if not 'blacklistedEngines' in all_locales:
      return

    blacklisted_search_engines = all_locales['blacklistedEngines']
    del dictionary['allLocales']['blacklistedEngines']

    self.delete_globally_blacklisted_search_engines_recursively(dictionary, blacklisted_search_engines)

  def override_search_engines_recursively(self, dictionary, overrides):
    for key, value in dictionary.items():
      if isinstance(value, dict):
        self.override_search_engines_recursively(value, overrides)
      else:
        if key == "visibleDefaultEngines":
          search_engines = value
          for search_engine, replacement_search_engine in overrides.items():
            if search_engine in search_engines:
              search_engines.remove(search_engine)
              if not replacement_search_engine in search_engines:
                search_engines.append(replacement_search_engine)
          dictionary[key] = search_engines

  def override_search_engines(self, dictionary):
    overrides = self.brave_model.overrides()
    self.override_search_engines_recursively(dictionary, overrides)

  def search_engine_exists_in_all_locales(self, search_engine):
    if search_engine in self.brave_model.search_engines_for_all_locales():
      return True

    return False

  def delete_search_engines_which_exist_in_all_locales(self, dictionary):
    locales = dictionary['locales']
    for locale in sorted(locales):
      for search_engine in locales[locale]['default']['visibleDefaultEngines']:
        if self.search_engine_exists_in_all_locales(search_engine):
          self.delete_search_engine_for_locale(dictionary, search_engine, locale)

  def search_engines(self, dictionary):
    search_engines = {}

    all_locales_search_engines = dictionary['allLocales']['visibleDefaultEngines']
    for search_engine in all_locales_search_engines:
      filename = search_engine + ".xml"
      if filename in search_engines:
        search_engines[filename] += 1
      else:
        search_engines[filename] = 1

    default_search_engines = dictionary['default']['visibleDefaultEngines']
    for search_engine in default_search_engines:
      filename = search_engine + ".xml"
      if filename in search_engines:
        search_engines[filename] += 1
      else:
        search_engines[filename] = 1

    locales = dictionary['locales']
    for locale in locales:
      for search_engine in locales[locale]['default']['visibleDefaultEngines']:
        filename = search_engine + ".xml"
        if filename in search_engines:
          search_engines[filename] += 1
        else:
          search_engines[filename] = 1

    region_overrides = dictionary['regionOverrides']
    for region in region_overrides:
      for search_engine in region_overrides[region]:
        search_engine_override = region_overrides[region][search_engine]
        filename = search_engine_override + ".xml"
        if filename in search_engines:
          search_engines[filename] += 1
        else:
          search_engines[filename] = 1

    return search_engines
