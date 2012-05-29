============
 Hieroglyph
============

.. slides::

   .. figure:: /_static/hieroglyphs.jpg
      :class: fill

      CC BY-SA http://www.flickr.com/photos/tamburix/2900909093/

**Hieroglyph** is an extension for Sphinx which builds HTML5 slides
from ReStructured Text documents.

.. notslides::

   This document provides a basic overview of Hieroglyph; dive deeper
   with the following documents:

   .. toctree::
      :maxdepth: 2

      config
      styling
      advanced
      ref-index

Why?
====

- You're already writing documentation using Sphinx
- You want to keep your presentation content in sync with other
  documentation
- You want slides that look beautiful
- Why Not?

Using Hieroglyph
================

Add **Hieroglyph** as a Sphinx extension to your configuration::

  extensions = [
      'hieroglyph',
  ]

Build your slides::

  $ sphinx -b html5slides output/slides

Adding Hieroglyph to your Makefile
----------------------------------

You make optionally want to add the following to your ``Makefile``::

  slides:
          $(SPHINXBUILD) -b slides $(ALLSPHINXOPTS) $(BUILDDIR)/slides
          @echo "Build finished. The HTML slides are in $(BUILDDIR)/slides."

  dirslides:
          $(SPHINXBUILD) -b dirslides $(ALLSPHINXOPTS) $(BUILDDIR)/slides
          @echo "Build finished. The HTML slides are in $(BUILDDIR)/slides."

(Don't forget, ``Makefiles`` love tabs!)

Writing Your Document
=====================

- By default, first and second level headings become slides
- The default theme styles these differently for topic breaks
- Otherwise it's just ReStructured Text!

Incremental Slides
------------------

.. rst-class:: build

- Adding the ``build`` class to a container
- To incrementally show its contents
- Remember that *Sphinx* maps the basic ``class`` directive to ``rst-class``

Slide-Only (and non-slide) Content
----------------------------------

Two directives let you restrict whether content is included::

  .. slides::


  .. notslides::


Styling Slides
==============

- Slides are just HTML, so you can write CSS to style them, either
  individually or as a whole
- You can add a custom CSS file to most themes by adding a
  ``custom_css`` theme options::

    slide_theme_options = {'custom_css':'custom.css'}

- Custom CSS files are contained in your documentation's static files
  directory (usually ``_static``)

Themes
------

Hieroglyph includes two themes_:

``slides``

  Two slides levels: the first level of headers become "section"
  headers, and the second become the real content.

``single-level``

  Only one style of slide, every slide has a title at the top.

See :ref:`hieroglyph-themes` for more information on using themes and
writing your own.

.. _themes: http://sphinx.pocoo.org/theming.html

Settings
========

**Hieroglyph** has some configuration dials you can turn to customize
the output. In addition to the theme, you can configure:

- The number of levels of headings which become slides
- Linking between slides and HTML documentation

See :ref:`hieroglyph-configuration` for more information.

License
=======

**Hieroglyph** is made available under a BSD license; see LICENSE for
details.

Included slide CSS and javascript licensed under the Apache Public
License. See http://code.google.com/p/html5slides/.

More Information
================

* `Sphinx`_
* `Docutils`_
* `rst2s5`_
* `HTML 5 Slides Project`_

.. _Sphinx: http://sphinx.pocoo.org/
.. _docutils: http://docutils.sourceforge.net/
.. _rst2s5: http://docutils.sourceforge.net/docs/user/slide-shows.html
.. _ifconfig: http://sphinx.pocoo.org/ext/ifconfig.html
.. _`HTML 5 Slides Project`: http://code.google.com/p/html5slides/
