============
 hieroglyph
============

**hieroglyph** is an extension for Sphinx which builds HTML5 slides
from ReStructured Text documents.


Using
=====

Add **hieroglyph** as a Sphinx extension to your configuration::

  extensions = [
      'hieroglyph',
  ]

Build your slides::

  $ sphinx -b html5slides output/slides

You make optionally want to add the following to your ``Makefile``::

  slides:
          $(SPHINXBUILD) -b html5slides $(ALLSPHINXOPTS) $(BUILDDIR)/slides
          @echo "Build finished. The HTML slides are in $(BUILDDIR)/slides."


Document Structure
==================

First and second level headings become slides


License
=======

**hieroglyph** is made available under a BSD license; see LICENSE for
details.

Included slide CSS and javascript licensed under the Apache Public
License. See http://code.google.com/p/html5slides/.
