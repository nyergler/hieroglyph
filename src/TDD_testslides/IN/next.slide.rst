=================
Slide & nextslide
=================

Some text

REF
====

.. nextslide:: DEMO

qaz

slide
=====

(empty)

.. slide:: SlideTitle

   slide with title

.. slide:: Always
   :inline-contents: True

   slide (inline-contents)

.. slide::

   slide (without a title)

BUG
====

.. slide:: Slide-slide

   note, there is a line after this slide

This line is lost (BUG)


NextSlides
==========

echo NextSlides

.. nextslide::
   :increment:

echo nextslide, increment

NextSlides H3
=============

H3
--

echo h3

.. nextslide::
   :increment:

This should be on a new slide, named `NextSlides H3 (2)`


Slide+next
==========

.. slide:: new

   echo slide:: new

.. nextslide::
   :increment:

echo  nextslide:: (increment)

.. nextslide::
   :increment:

echo  nextslide:: (increment)

Nested
-------

.. slide:: new

   echo slide:: new

   .. nextslide::
      :increment:

   echo  nextslide:: (increment)

   .. nextslide::
      :increment:

   echo  nextslide:: (increment)

Nextslide with auto
===================

still with BUG!

Before nextslide
----------------

.. nextslide::
   :increment

After nextslide
---------------

This should be a new slide!

With title `Nextslide with auto (2)` and a header `After nextslide`


END
===

That is all folks

