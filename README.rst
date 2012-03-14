============
 hieroglyph
============

**hieroglyph** is an extension for Sphinx which builds HTML5 slides
from ReStructured Text documents.

Installing
==========

You can install **hieroglyph** using ``easy_install`` or ``pip``::

   $ easy_install hieroglyph

You can also download the `latest development version`_, which may
contain new features.

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

.. _`latest development version`: https://github.com/nyergler/hieroglyph/tarball/master#egg=hieroglyph-dev
