.. _builders:

=====================
 Hieroglyph Builders
=====================

In Sphinx parlance, a "builder" is an output target. Sphinx includes
several of its own, including ones for HTML pages, ePub documents, and
PDF. Hieroglyph adds two types of additional builders: slides and
inline slides. Each supports building HTML documents or
``index.html`` documents in directories (useful if you prefer URLs
without ".html" in them).


Slide Builder
=============

The slide builders, ``slides``, and ``dirslides``, create slide show
documents for each of the source files.

You may add one (or both) of the following targets to your
``Makefile`` to enabled one of these targets::

  slides:
          $(SPHINXBUILD) -b slides $(ALLSPHINXOPTS) $(BUILDDIR)/slides
          @echo "Build finished. The HTML slides are in $(BUILDDIR)/slides."

  dirslides:
          $(SPHINXBUILD) -b dirslides $(ALLSPHINXOPTS) $(BUILDDIR)/slides
          @echo "Build finished. The HTML slides are in $(BUILDDIR)/slides."


The output of these builders includes support for the slide table and
presenter's console. If ``autoslides`` is enabled, sections in the
source files will be transformed into slides. If ``autoslides`` is not
enabled, only content found in ``slide`` directives will be in the output.

See :ref:`slide-directive` for more information.

Inline Slide Builder
====================

The inline slide builders add support for the ``slide`` directive to
the stock HTML builders, and add an additional stylesheet to the
output for basic inline display.

You may add one (or both) of the following targets to your
``Makefile`` to enabled one of these targets::

  inlineslides:
          $(SPHINXBUILD) -b inlineslides $(ALLSPHINXOPTS) $(BUILDDIR)/slides
          @echo "Build finished. The HTML output is in $(BUILDDIR)/slides."

  dirinlineslides:
          $(SPHINXBUILD) -b dirinlineslides $(ALLSPHINXOPTS) $(BUILDDIR)/slides
          @echo "Build finished. The HTML output is in $(BUILDDIR)/slides."


When using one of the inline builders, ``autoslides`` functionality is
disabled.
