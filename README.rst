============
 hieroglyph
============

**hieroglyph** is an extension for Sphinx which builds HTML5 slides
from ReStructured Text documents.


Using Hieroglyph
================

Add **hieroglyph** as a Sphinx extension to your configuration::

  extensions = [
      'hieroglyph',
  ]

Build your slides::

  $ sphinx -b html5slides output/slides


License
=======

**hieroglyph** is made available under a BSD license; see LICENSE for
details.

Included slide CSS and javascript licensed under the Apache Public
License. See http://code.google.com/p/html5slides/.
