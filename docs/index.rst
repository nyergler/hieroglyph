============
 Hieroglyph
============

.. slides::

   .. figure:: /_static/hieroglyphs.jpg
      :class: fill

      CC BY-SA http://www.flickr.com/photos/tamburix/2900909093/

Hieroglyph is an extension for `Sphinx`_ which builds HTML slides from
`ReStructured Text`_ documents.

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

Install from `PyPI`_ (or `github`_)::

  pip install hieroglyph

Add **Hieroglyph** as a Sphinx extension to your configuration::

  extensions = [
      'hieroglyph',
  ]

Build your slides::

  $ sphinx-build -b slides output/slides

.. _`PyPI`: http://pypi.python.org/pypi/hieroglyph
.. _`github`: http://github.com/nyergler/hieroglyph

Adding Hieroglyph to your Makefile
----------------------------------

You make optionally want to add the following to your ``Makefile``::

  slides:
          $(SPHINXBUILD) -b slides $(ALLSPHINXOPTS) $(BUILDDIR)/slides
          @echo "Build finished. The HTML slides are in $(BUILDDIR)/slides."

You can also build using directories.

.. notslides::

   The directory builder is analogous to Sphinx's `HTML Directory
   builder`_ . Each document is placed in its own directory as
   index.html, which allows you to omit the file from the URL.

   You can add this to the ``Makefile`` with the following.

::

  dirslides:
          $(SPHINXBUILD) -b dirslides $(ALLSPHINXOPTS) $(BUILDDIR)/slides
          @echo "Build finished. The HTML slides are in $(BUILDDIR)/slides."

(Don't forget, ``Makefiles`` love tabs!)

.. _`HTML Directory Builder`: http://sphinx.pocoo.org/builders.html#sphinx.builders.html.DirectoryHTMLBuilder

Writing Your Document
=====================

- First and second level headings become slides
- Default theme styles these differently for topic breaks
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

- The number of heading levels which become slides
- Linking between slides and HTML documentation

See :ref:`hieroglyph-configuration` for more information.

Presenter Console
=================

Hieroglyph includes a simple presenter console to make it easier to
use when presenting slides.

**To activate the console, press "c" when viewing the slides.**

The console will open in a new window. Advancing the slides in either
window will update the other one, as well.

License
=======

**Hieroglyph** is made available under a BSD license; see LICENSE for
details.

Included slide CSS and JavaScript originally based on `HTML 5 Slides`_
licensed under the Apache Public License.

More Information
================

* `Sphinx`_
* `Docutils`_
* `rst2s5`_
* `HTML 5 Slides`_

.. _Sphinx: http://sphinx.pocoo.org/
.. _docutils: http://docutils.sourceforge.net/
.. _rst2s5: http://docutils.sourceforge.net/docs/user/slide-shows.html
.. _ifconfig: http://sphinx.pocoo.org/ext/ifconfig.html
.. _`HTML 5 Slides`: http://code.google.com/p/html5slides/
.. _`ReStructured Text`: http://docutils.sourceforge.net/
