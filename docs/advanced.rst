================
 Advanced Usage
================

.. ifslides::

   .. figure:: /_static/hieroglyphs.jpg
      :class: fill

      CC BY-SA http://www.flickr.com/photos/tamburix/2900909093/

.. _slide-directive:

The ``slide`` directive
=======================

Instead of (or in addition to) section headings, Hieroglyph also
includes a directive that may be used to indicate a Slide should be
created. The directive may have a title specified, as well as a level
parameter.

For example::

  .. slide:: The Slide Title
     :level: 2

     This Slide would appear as a level two slide.


.. _interlinking-html:

Interlinking HTML Output
========================

.. ifslides::

   - If you build both slides and HTML output, Hieroglyph can create
     links between them.
   - You need to use the corresponding builders: i.e.,
     ``SlideBuilder`` and ``StandaloneHTMLBuilder``

.. ifnotslides::

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


.. _document-configuration:

Per-File Configuration
======================

When working with multi-file projects, there may be cases when it is
desirable to override the theme or set configuration value for
specific files. This can be accomplished using the
:rst:dir:`slideconf` directive::

  .. slideconf::
     :theme: single-level

Values specified in a ``slideconf`` directive override defaults
specified in ``conf.py``. If more than one ``slideconf`` appears in a
document, only the last one is used.
