================
 Theme Features
================

Slides & Single Level
=====================

Displaying Images
-----------------

.. slide:: Displaying Images
   :level: 2

   * Images and static assets should go in the ``_static`` directory in
     your project
   * The :rst:dir:`image` directive lets you display an image
   * Hieroglyph includes support for showing an image full size in a
     slide (like the title slide in this deck).

   ::

     .. figure:: /_static/hieroglyphs.jpg
        :class: fill

        CC BY-SA http://www.flickr.com/photos/tamburix/2900909093/

You can include any image in a slide using the :rst:dir:`image`
directive. Just drop them in the ``_static`` directory in your
project.

Hieroglyph also includes some support for showing an image as the full
slide using the :rst:dir:`figure` directive. For example, the
Hieroglyph introductory slide deck uses the following markup::

  .. figure:: /_static/hieroglyphs.jpg
     :class: fill

     CC BY-SA http://www.flickr.com/photos/tamburix/2900909093/

The caption (license information above) is styled as an overlay on the
image.


Included Styles
---------------

Hieroglyph includes some classes that for styling slides:

* ``appear``

   Case the slide to just appear, replacing the previous slide,
   instead of sliding from the right to left.

* ``fade-in``

   Causes the slide to quickly fade in and out, instead of sliding
   from the right to left.


.. _org_doc_gio_slides:

Slides2
=======

The ``slides2`` theme was added in Hieroglyph 0.7, and as based on the
`Google I/O 2012+`_ HTML slide templates. Also see: :doc:`gio_slides`

Theme Options
-------------

The ``slides2`` theme requires presentation metadata in the
``conf.py`` file. You can specify one or more presenters; presenter
information will be included on the title and end slides
automatically.

.. code-block:: python

   slide_theme_options = {
       'presenters': [
           {
               'name': 'The Author',
               'twitter': '@author',
               'www': 'http://example.com/author',
               'github': 'http://github.com/author/example'
           },
       ],
   }

In addition to the presenter metadata, the following options may be
specified in ``slide_theme_options``:

``subtitle``
    Default: ``""``

    The presentation title will be taken from ``conf.py``; if you
    would like to display a sub-title on the title slide, specify it
    here.

``use_builds``
    Default: ``true``

``use_prettify``
    Default: ``true``

``enable_slide_areas``
    Default: ``true``

``enable_touch``
    Default: ``true``

``favicon``
    Default: ``""``


Title & End Slides
------------------

The title and end slides contain presentation metadata and links.
Unlike the other slides, they are generated directly from template
fragments. You can override these by providing a ``title_slide.html``
or ``end_slide.html`` template in the ``_templates`` directory of your
project.

For example, ``title_slide.html`` with a full-bleed background image
might look like this::

  <slide class="title-slide segue nobackground fill"
         style="background-image: url(_static/insect_trap.jpg)">
    <hgroup class="auto-fadein">
      <h1 class="white" data-config-title><!-- populated from slide_config.json --></h1>
      <h2 data-config-subtitle><!-- populated from slide_config.json --></h2>
      <h2 data-config-presenter><!-- populated from slide_config.json --></h2>
    </hgroup>
    <footer class="source white">
      CC BY-NC-SA // www.flickr.com/photos/boobook48/5041751802/
    </footer>

  </slide>

An ``end_slide.html`` template might look like this::

  <slide class="thank-you-slide segue nobackground">
    <article class="flexbox vleft auto-fadein">
      <h2>Thank You!</h2>
    </article>
    <p class="auto-fadein" data-config-contact>
      <!-- populated from slide_config.json -->
    </p>
  </slide>

Displaying Images
-----------------

Included Styles
---------------

Incremental Slides (Builds)
---------------------------

In addition to the :ref:`common incremental slide support
<incremental_slides>`, the ``slides2`` theme supports more granular
builds. Items with the class ``build-item-x`` (where ``x`` is a
number) will be incrementally display, in numerical order.

For example, you can show items from bottom to top on a slide::

  .. rst-class:: build-item-3

  This will be shown third

  .. rst-class:: build-item-2

  This will be shown second

  .. rst-class:: build-item-1

  This will be shown first

If multiple items have the same number, they will both be displayed at
the same time.

.. warning::

   ``build-item-*-only`` and ``build-item-*class-*`` are experimental
   and their behavior may change considerably as we learn more.

Items may also be displayed *only* at a specific index. That is,
displayed, then hidden again. Appending the suffix ``-only`` to the
``build-item-`` class activates this behavior.


.. _`Google I/O 2012+`: https://code.google.com/p/io-2012-slides/
