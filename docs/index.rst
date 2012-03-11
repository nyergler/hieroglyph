============
 hieroglyph
============

.. ifconfig:: builder == 'html5slides'

   .. figure:: /_static/hieroglyphs.jpg
      :class: fill

      CC BY-SA http://www.flickr.com/photos/tamburix/2900909093/

**hieroglyph** is an extension for Sphinx which builds HTML5 slides
from ReStructured Text documents.

.. toctree::
   :maxdepth: 2


Why?
====

- You're already writing documentation using Sphinx
- You want to keep your presentation content in sync with other
  documentation
- You want slides that look beautiful
- Why Not?

Using Hieroglyph
================

Add **hieroglyph** as a Sphinx extension to your configuration::

  extensions = [
      'hieroglyph',
  ]

Build your slides::

  $ sphinx -b html5slides output/slides

Adding Hieroglyph to your Makefile
----------------------------------

You make optionally want to add the following to your ``Makefile``::

  slides:
          $(SPHINXBUILD) -b html5slides $(ALLSPHINXOPTS) $(BUILDDIR)/slides
          @echo "Build finished. The HTML slides are in $(BUILDDIR)/slides."

(Don't forget ``Makefiles`` love tabs!)

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

Handout Content
---------------

Currently::

  .. ifconfig:: build != 'html5slides'

     Non-slide content here

This requires that you enable the `ifconfig`_ extension.

Perhaps one day we'll provide something like the rst2s5's
``.. handout ::`` directive.


Styling Slides
==============

- Slides are contained in ``<article>`` elements
- The heading level is added as a class; ie, ``level-2``
- You can add a custom CSS file to most themes by adding a
  ``custom_css`` theme options::

    slide_theme_options = {'custom_css':'custom.css'}

- Custom CSS files are contained in your documentation's static files
  directory (usually ``_static``)

Themes
------

Hieroglyph includes two `themes <http://sphinx.pocoo.org/theming.html>`_:

``slides``

  Two slides levels: the first level of headers become "section"
  headers, and the second become the real content.

``single-level``

  Only one style of slide, every slide has a title at the top.

Setting the Theme
-----------------

You can set your theme using the ``slide_theme`` configuration
setting.

::

  slide_theme = 'single-level'

If you're using a custom theme, you can also set the directory to look
in for themes::

  slide_theme_path = '...'

Settings
========

``slide_theme``

  The theme to use when generating slides. Default: ``slides``

``slide_levels``

  Number of heading levels to convert to slides; note that the
  document title is level 1. Default: 3

``slide_theme_options``

  Theme specific options as a ``dict``; default: {}

``slide_theme_path``

  The path to look for themes in; default: None.

License
=======

**hieroglyph** is made available under a BSD license; see LICENSE for
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


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
