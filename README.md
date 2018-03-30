hfeed2atom
===========

Convert h-feed pages to Atom 1.0 XML format for traditional feed readers. You can try it out at https://kartikprabhu.com/hfeed2atom

Installation
------------

To install hfeed2atom use pip as follows:

```
pip install git+https://github.com/kartikprabhu/hfeed2atom.git --process-dependency-links

```

This will install hfeed2atom with its dependencies from pypi and mf2py from the experimental repo https://github.com/kartikprabhu/mf2py/tree/experimental.

Usage
-----

hfeed2atom takes as arguments one or more of the following:
* `doc`: a string, a Python File object or a BeautifulSoup document containing the contents of an HTML page
* `url`: the URL for the page to be parsed. It is recommended to always send a URL argument as it is used to convert all other URLs in the document to absolute URLs.
* `atom_url`: the URL of the page with the ATOM file.
* `hfeed`: a Python dictionary of the microformats h-feed object. Use this if the document has already been parsed for microformats.
 
hfeed2atom returns the following as a tuple:
* Atom format of the h-feed, or None if there was an error.
* A string message of the error if any


The easiest way to use hfeed2atom in your own python code to parse the feed on a URL `http://example.com`

```
from hfeed2atom import hfeed2atom

atom, message = hfeed2atom(url = 'http://example.com')
```
With this code, hfeed2atom will do a GET request to `http://example.com`, find the first h-feed and return the Atom as a string.

If you already have the `contents` of the URL (by doing a GET request yourself, or if it is your own page on your server), then you can pass them as a `doc` argument as

```
atom, message = hfeed2atom(doc = contents, url = 'http://example.com')
```
`doc` can be a string, a Python File object or a BeautifulSoup document.

If you already have the h-feed microformats object of a page as a Python dictionary in the variable `hfeed` then use

```
atom, message = hfeed2atom(hfeed = hfeed, url = 'http://example.com')
```
Note, in this case hfeed2atom assumes that all the required properties for Atom are already in the `hfeed` variable and *will not* attempt to generate any fallback properties.

Features
--------

* Finds first h-feed element to generate Atom feed, if no h-feed found defaults to using the top-level h-entries for the feed.
* Generates fallbacks for required Atom properties of the feed. The fallbacks, in order, are:
  - title : h-feed `name` property else, `<title>` element of the page else, `Feed for URL`.
  - id : h-feed `uid` or `url` property else, URL argument given.
  - updated date : h-feed `updated` or `published` property else, `updated` or `published` property of the latest entry.
* Generates fallback categories for the h-feed from the `meta name='keywords'>` element of the page.
* Generates fallback for required Atom properties of each entry in the h-feed. The fallbacks, in order, are:
  - title : h-entry `name` property if it is not same as `content>value` else, `content` property truncated to 50 characters else, `uid` or `url` of the entry.
  - id : h-entry `uid` property or `url` property else, error and skips that entry.
  - updated date : h-entry `updated` or `published` property else, error and skips that entry.

To Do
-----
* Author discovery if the h-feed does not have an author property. Note `<author>` is an optional tag in Atom!

Go forth
--------

Now [use this yourself](https://github.com/kartikprabhu/hfeed2atom) and [give feedback](https://github.com/kartikprabhu/hfeed2atom/issues).
