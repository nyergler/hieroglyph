===
All
===

Note: For this demo the conf should contain `slide_levels = 2`

H2-1 This will become a the first h1
====================================

on a new slide

H2-2 This should be a new slide, again with a h2 header
=======================================================

The H2-2 line is missing!

H3 But this H3 is shown instead
-------------------------------

There should be a (h3) header above this line


H2-3 Again
==========

A new side

H2-4 More missing lines
=======================

The lines H2-4 and H3-1 will be gone ...

H3-1 First h3
-------------

This is shown (but not H3-1)

H3-2 Second h3
--------------

This is shown (as well as H3-2, as slide title)



H2-5 Now with h2+3+4
====================

Reset again (new H2 slide)

H2-6 Demo
=========

Echo: H2-6 Demo

H3 A h2 with an h4
------------------

Echo: H3 A h2 with an h4

H4 What does happen?
^^^^^^^^^^^^^^^^^^^^

Echo: H4 What does happen?


H2-7 slide
==========

Echo H2-7 slide

.. slide:: Title

   Some body 

.. slide:: another slide 

   With a title

.. slide::

   Thise `slide` slide has no title

H2-8 nextslide
==============

echo H2-8 nextslide

.. nextslide::
   :increment:

echo  nextslide (without title, increment)

.. nextslide:: next

echo  nextslide (with title: next)




.. ifslides::
   ..nextslide:: Title

   echo DOT DOT slide COLON COLON Title

   
.. slide:: another slide

   echo DOT DOT slide COLON COLON another slide

.. slide::

   echo DOT DOT slide

   Thise `slide` slide has no title

H2 nextslide
============

echo H2 nextslide

.. nextslide::
   :increment:

echo DOT DOT nextslide
Text on **nextslide**






OLD
===
.. notslides::

   oud

.. slides::

  oud
