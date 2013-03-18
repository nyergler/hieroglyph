.. _builders:

=====================
 Hieroglyph Builders
=====================

In Sphinx parlance, a "builder" is an output target. Sphinx includes
`several of its own`_, including ones for HTML pages, ePub documents,
and PDF.

.. _`several of its own`: http://sphinx-doc.org/builders.html

Hieroglyph adds additional builders for generating slides. The
builder's "name" must be given to the **-b** command-line option of
:program:`sphinx-build` to select a builder.

You may want to add one (or more) of the Hieroglyph builders to your
``Makefile`` to make it easier to run the Sphinx builder.

For example, to add the ``slides`` builder to your Makefile, add the
following target::

  slides:
          $(SPHINXBUILD) -b slides $(ALLSPHINXOPTS) $(BUILDDIR)/slides
          @echo "Build finished. The HTML slides are in $(BUILDDIR)/slides."

(Remember, makefiles are indented using tabs, not spaces.)

.. automodule:: hieroglyph.builder

.. autoclass:: SlideBuilder

.. autoclass:: DirectorySlideBuilder

.. autoclass:: InlineSlideBuilder

.. autoclass:: DirectoryInlineSlideBuilder

Abstract Builders
=================

Hieroglyph also defines two abstract builders. These classes are not
capable of building slides on their own, but encapsulate most of the
slide-specific functionality.

.. autoclass:: AbstractSlideBuilder
   :members:

.. autoclass:: AbstractInlineSlideBuilder
   :members:
