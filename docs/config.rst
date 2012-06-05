.. _hieroglyph-configuration:

==========================
 Hieroglyph Configuration
==========================

.. slides::

   .. figure:: /_static/hieroglyphs.jpg
      :class: fill

      CC BY-SA http://www.flickr.com/photos/tamburix/2900909093/

Basic Configuration
===================

``slide_theme``

  The theme to use when generating slides. Default: ``slides``

``slide_levels``

  Number of heading levels to convert to slides; note that the
  document title is level 1. Heading levels greater than slide levels
  will simply be treated as slide content.

  Default: 3

Themes
======

``slide_theme_options``

  Theme specific options as a ``dict``; default: ``{}``

  See :ref:`custom-css` for more information.

``slide_theme_path``

  The path to look for themes in; default: ``[]``.

For more information on styling and themes, see
:ref:`hieroglyph-themes`.


.. _configuring-interlinking:

Interlinking HTML Output
========================

:ref:`interlinking-html` can be enabled for slides, HTML, or both.

``slide_link_to_html``

  Link from slides to HTML; default: ``False``.

``slide_link_html_to_slides``

  Link from HTML to slides; default: ``False``

``slide_link_html_sections_to_slides``

  Link individual HTML sections to specific slides; default: ``False``

  .. notslides::

     Note that ``slide_link_html_to_slides`` must be enabled for this
     to have any effect.

Relative Paths
--------------

The slide/HTML interlinking needs to know how to find the slide and
HTML output from the other side. There are two configuration
parameters for this. They're configured to work with Sphinx and
Hieroglyph's standard configuration (output in sub-directories of a
common build directory) by default .

``slides_relative_path``

  Relative path from HTML to slides; default: ``../slides/``

``slides_html_relative_path``

  Relative path from slides to HTML; default: ``../html/``

Additional Paramters
--------------------

``slides_html_slide_link_symbol``

  Text used to link between HTML sections and slides.

  This text is appended to the headings, similar to the section links
  in HTML output.

  Default: §
