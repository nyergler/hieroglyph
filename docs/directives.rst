============
 Directives
============

.. rst:directive:: .. ifslides::

   Include the directive contents in the output only when building
   slides. That is, when one of the :ref:`builders` is used.

.. rst:directive:: .. ifnotslides::

   Exclude the contents of the directive from output when building
   slides. That is, when one of the :ref:`builders` is used.

.. note::

   :rst:dir:`ifslides` and :rst:dir:`ifnotslides` were originally
   named ``slides`` and ``notslides``, respectively. They were renamed
   prior to the addition of the :rst:dir:`slide` directive, in order
   to be more explicit.

   The old names work, but will show a warning during the build
   process. Expect the old names to be removed in some future version.

.. rst:directive:: .. slideconf::

   Configure slide-related options for the current document.

   Some of the :ref:`hieroglyph-configuration` options can be
   overridden on a per document basis.

   The ``theme`` option, if present, will set the theme for document.
   See the :ref:`theme documentation <hieroglyph-themes>` for more
   information on themes.

   The ``autoslides`` option, if present, must be ``True`` or
   ``False``. If set to ``True``, slides will be generated from the
   document headings and contents. If ``autoslides`` is ``False``,
   slides will only be created with Sphinx encounters the
   :ref:`slide-directive`.

   The ``slide_classes`` option allows you to specify classes that
   will be added to slides by default. This allows you, for example,
   to add a class that applies some styling to the slides. Note that
   if a slide has an explicit class set (ie, with the
   :rst:dir:`rst-class` directive), the classes specified here *will
   not* be applied.

   See :ref:`document-configuration` for more information and
   examples.

.. rst:directive:: .. slide:: title

   Create a slide in the document. The directive takes the slide title
   as its argument, and some optional settings for the slide. For
   example::

     .. slide:: Example Slide
        :level: 2

        This is an example slide.

        * Bullet 1
        * Bullet 2

   The ``level`` option, if present, will set the level of the slide,
   which is used for :ref:`styling slides <hieroglyph-themes>`.

   By default, content contained in a ``slide`` directive will be
   excluded when building non-slide output. You can change this
   behavior by setting the ``inline-contents`` option to ``True``.
   When ``inline-contents`` is set to ``True``, the contents of the
   ``slide`` directive will be included in all output.

   The ``class`` option, if present, will add the given class to the
   slide output.

   The following example will set the class ``red-slide`` on the slide
   output, and include the slide content (the sentence and the
   bulleted listed, but not the title)  in HTML output.

   ::

     .. slide:: Warning!
        :level: 2
        :class: red-slide
        :inline-contents: True

        This error can occur when:

        * Microwaving metal
        * Leaving the gas on
        * Using a frayed electrical cord

.. rst:directive:: .. nextslide:: title

   Splits the content at the directive when building slides. An option
   title may be specified as an argument. If not specified, the title
   of the current section will be copied.

   Consider the following example::

     Section Title
     =============

     some content

     .. nextslide::

     additional content

   When building slides, this will generate two slides with the name
   **Section Title**.

   The ``increment`` argument, if present, will append an index to the
   slide title.
