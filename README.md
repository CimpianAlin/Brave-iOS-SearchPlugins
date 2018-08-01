# Search Plugins

Locale-based search engines are imported from the Mozilla Android l10n repos and merged with the Brave search engines as specified in `brave.json`. To update the Brave-iOS-SearchPlugins repo to the latest set of search engines from Mozilla, execute the `./update-search-engines.py` script.

```
usage: update_search_engines.py [-h] [-s]

optional arguments:
  -h, --help    show this help message and exit
  -s, --scrape  Scrape Mozilla for latest search plugins
```

*Do not make changes to any files in `iOSFinalResult` and `MozillaOriginals/SearchPlugins` -- these changes will be overwritten on the next import!* If you need to make changes to search plugins, you have the following options (in preferred order):

1. Define an overlay in `MozillaOriginals/SearchOverlays`. Overlays allow local, iOS-specific modifications to be applied after the files are imported. See README.md in `MozillaOriginals` directory for Search Overlay API documentation
2. Add new search engines to the `BraveOverrides` directory and reference these search engines in the `brave.json` file under the `allLocales/visibleDefaultEngines` node or a specific locale node, i.e. `locales/en-US/default/visibleDefaultEngines`
3. Add references to search engines in the `brave.json` file under the `allLocales/visibleDefaultEngines` node or a specific locale node, i.e. `locales/en-US/default/visibleDefaultEngines`

## Adding a search engine to all locales

You can add a search engine to all locales by referencing the search engine in the `brave.json` file under the `allLocales/visibleDefaultEngines` node as follows:

```
"allLocales": {
  "visibleDefaultEngines": [
    "duckduckgo",
    "github",
    "infogalactic",
    "qwant",
    "semanticscholar",
    "stackoverflow",
    "startpage",
    "wolframalpha",
    "youtube"
  ]
```

## Specifying a default search engine

The global default search engine should be specified in the `brave.json` file under the `locales/default/searchDefault` node as follows:

```
"locales": {
  "default": {
    "searchDefault": "Google"
  }
}
```

or you can override the global search engine on a per region basis under the `locales/<LOCALE>/<REGION>/searchDefault` node as follows:

```
"locales": {
  "be": {
    "BY": {
      "searchDefault": "Яндекс"
    },
    "KZ": {
      "searchDefault": "Яндекс"
    },
    "RU": {
      "searchDefault": "Яндекс"
    },
    "TR": {
      "searchDefault": "Яндекс"
    }
  }
}
```

## Unsupported locales

Default search engines are used when a locale is not supported and should be added to the `brave.json` file under the `locales/default/visibleDefaultEngines` node, as follows:

```
"locales": {
  "default": {
    "visibleDefaultEngines": [
      "google",
      "bing",
      "amazondotcom",
      "twitter",
      "wikipedia",
      "yahoo"
    ]
  }
}
```

## Overridding search engines globally

Search engines can be overridden globally by adding search engines to the `overrides` node as follows:

```
"overrides": {
  "google-nocodes": "google"
}
```

## Overridding search engines for a specific region

Search engines can be overridden on a per region basis by adding a `<REGION>` node to the `regionOverrides` node as follows, region overrides only occur within the iOS application:

```
"regionOverrides": {
  "GB": {
    "yahoo": "yahoo-en-GB"
  }
}
```

## Blacklisting search engines

Mozilla Android l10n search engines can be blacklisted for all locales by adding a `blacklistedEngines` node to the `"allLocales"` node, as follows:

```
"allLocales": {
  "blacklistedEngines": [
    "foo",
    "bar"
  ]
}
```

or you can blacklist a search engine on a per locale basis by adding a `blacklistedEngines` node to the `locales/<LOCALE>` node as follows:

```
"locales": {
  "en": {
    "blacklistedEngines": [
      "foobar"
    ]
  }
}
```
