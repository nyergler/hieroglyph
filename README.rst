============
 Hieroglyph
============

**Hieroglyph** is an extension for `Sphinx`_ which builds HTML5 slides
from ReStructured Text documents.

Installing
==========

You can install **Hieroglyph** using ``easy_install`` or ``pip``::

   $ easy_install hieroglyph

You can also download the `latest development version`_, which may
contain new features.

Using Hieroglyph
================

Add **Hieroglyph** as a Sphinx extension to your configuration::

  extensions = [
      'hieroglyph',
  ]

Build your slides::

  $ sphinx-build -b slides sourcedir outdir

Where ``sourcedir`` is the directory containing the Sphinx ``conf.py``
file and ``outdir`` is where you want your slides to output to.


License
=======

**Hieroglyph** is made available under a BSD license; see LICENSE for
details.

Included slide CSS and javascript licensed under the Apache Public
License. See http://code.google.com/p/html5slides/.

.. _`Sphinx`: http://sphinx.pocoo.org/
.. _`latest development version`: https://github.com/nyergler/hieroglyph/tarball/master#egg=hieroglyph-dev
