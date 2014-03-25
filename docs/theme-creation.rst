
.. _custom-themes:

==================
 Creating  Themes
==================

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

Hieroglyph also allows specification of extra pages to build in the
theme configuration. Any key in ``options`` that begins with
``extra_pages_`` specifies an additional page to be built. The base
``slides`` theme specifies the console in this manner::

  [options]
  custom_css =
  custom_js =
  extra_pages_console = console.html

The value of the key (``console.html`` in this case) specifies the
template to use to render the page.

See the Sphinx documentation for `themes`_ for more information.

.. _`themes`: http://sphinx.pocoo.org/theming.html
