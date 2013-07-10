.. slideconf::
   :autoslides: True
   :theme: single-level

=======================
 Hieroglyph Smoke Test
=======================

.. ifslides::

   .. figure:: /_static/hieroglyphs.jpg
      :class: fill

      CC BY-SA http://www.flickr.com/photos/tamburix/2900909093/

This is the Hieroglyph Smoke Test. It contains visual tests for
verifying Hieroglyph functionality.

.. ifnotslides::

   This section should not be included in slides.

Bulleted Lists
==============

- First Point
- Second Point
- Third Point

Another notation:

* First Point
* Second Point
* Third Point

Enumerated Lists
================

This list will be numbered:

#. First Point
#. Second Point
#. Third Point

This list will be lettered:

A. First Point
B. Second Point
#. Third Point

Nested Lists
------------

* First
* Second

  * Sub Item 1
  * Sub Item 2


Code Highlighting
=================

This block will be highlighted as Python:

.. code-block:: python

    def func(a):
        print 'The value of a is %(a)s' % locals()

This block will be highlighted as Javascript:

.. code-block:: javascript

   function func(a) {
       console.log('The value of a is ', a);
   }

This block will not be highlighted:

.. code-block:: none

   def func(a):
       """I am not highlighted."""

Admonitions
===========

The ``note`` admonition is used to create notes in the presenter console.

.. note::

   This is a *note* admonition. It will not appear in the slides.

.. warning::

   Warnings, however, stay where they belong.

.. note::

   Notes can appear anywhere in the slide content.


Hieroglyph Features
===================

The following slides test Hieroglyph features.

Incremental Slides
------------------

.. rst-class:: build

- Adding the ``build`` class to a container
- To incrementally show its contents
- Remember that *Sphinx* maps the basic ``class`` directive to ``rst-class``


.. slide:: The ``slide`` Directive
   :level: 2

   In addition to headings, you can use the ``..slide::`` directive to
   define a slide.

   A recursive example::

     .. slide:: The ``slide`` Directive
        :level: 2

        In addition to headings, you can use the ``..slide::`` directive to
        define a slide.

        A recursive example:
