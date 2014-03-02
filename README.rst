============
 Hieroglyph
============

.. image:: https://api.travis-ci.org/nyergler/hieroglyph.png?branch=master
   :target: https://travis-ci.org/nyergler/hieroglyph

.. image:: https://coveralls.io/repos/nyergler/hieroglyph/badge.png?branch=master
   :target: https://coveralls.io/r/nyergler/hieroglyph?branch=master


**Hieroglyph** is an extension for `Sphinx`_ which builds HTML5 slides
from ReStructured Text documents.

Installing
==========

You can install **Hieroglyph** using ``easy_install`` or ``pip``::

   $ easy_install hieroglyph

You can also download the `latest development version`_, which may
contain new features. Hieroglyph supports Python 2.7 and Python 3.3.

Using Hieroglyph
================

You can start a new **Hieroglyph** presentation using the included
quickstart script::

  $ hieroglyph-quickstart

This will generate the Sphinx configuration, along with an optional
Makefile and batch file, with Hieroglyph enabled.

If you're on something UNIX-like (Linux, Mac OS X, etc), you can then
generate your slides by running ``make``::

  $ make slides


You can also add **Hieroglyph** as a Sphinx extension to your
existing configuration::

  extensions = [
      'hieroglyph',
  ]


`Read the documentation`_ for all the details about using,
configuring, and extending Hieroglyph.

Connect
=======

You can connect with other Hieroglyph users and the developers via the
`hieroglyph-users`_ email list (Google Groups). A `Gmane archive`_ is
also available.

.. _`hieroglyph-users`: http://groups.google.com/d/forum/hieroglyph-users
.. _`Gmane archive`: http://dir.gmane.org/gmane.comp.python.hieroglyph.users

License
=======

**Hieroglyph** is made available under a BSD license; see LICENSE for
details.

Included slide CSS and JavaScript originally based on `HTML 5 Slides`_
licensed under the Apache Public License.

.. _`Sphinx`: http://sphinx.pocoo.org/
.. _`latest development version`: https://github.com/nyergler/hieroglyph/tarball/master#egg=hieroglyph-dev
.. _`HTML 5 Slides`: http://code.google.com/p/html5slides/
.. _`Read the documentation`: http://hieroglyph.io/
