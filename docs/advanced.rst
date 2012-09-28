================
 Advanced Usage
================

.. slides::

   .. figure:: /_static/hieroglyphs.jpg
      :class: fill

      CC BY-SA http://www.flickr.com/photos/tamburix/2900909093/


.. _interlinking-html:

Interlinking HTML Output
========================

.. slides::

   - If you build both slides and HTML output, Hieroglyph can create
     links between them.
   - You need to use the corresponding builders: i.e.,
     ``SlideBuilder`` and ``StandaloneHTMLBuilder``

.. notslides::

   Hieroglyph supports linking between slides and HTML output, such as
   from the Sphinx HTML builders. In order to do this successfully,
   the slide and HTML builders used must correspond to one
   another. That is, the ``SlideBuilder`` must be used with the
   ``StandaloneHTMLBuilder``, and the ``DirectorySlideBuilder`` must
   be used with the ``DirectoryHTMLBuilder``.

For example, runnning::

  $ make html slides

Will generate HTML and slides if interlinking is enabled. See
:ref:`configuring-interlinking` for information on enabling
interlinking in the configuration.


.. _custom-themes:

Custom Themes
=============

Hieroglyph themes are based on Sphinx's HTML `themes`_. Themes are
either a directory or zipfile, which contains a ``theme.conf`` file,
templates you wish to override, and a ``static/`` directory which
contains images, CSS, etc.

When defining a slide theme, inherit from the ``slides`` theme for
basic support. For example, the ``single-level`` them has the
following ``theme.conf``::

  [theme]
  inherit = slides
  stylesheet = single.css

  [options]
  custom_css =

In order to include the base slide styling, your theme's stylesheet
should begin with::

  @import url(slides.css);

``slides.css`` will be supplied by the base theme (``slides``).

See the Sphinx documentation for `themes`_ for more information.

.. _`themes`: http://sphinx.pocoo.org/theming.html


Per-File Configuration
======================

When working with multi-file projects, there may be cases when it is
desirable to override the theme or set configuration value for
specific files. This can be accomplished using the ``slideconf``
directive::

  .. slideconf::
     :theme: single-level

Values specified in a ``slideconf`` directive override defaults
specified in ``conf.py``. If more than one ``slideconf`` appears in a
document, only the last one is used.
