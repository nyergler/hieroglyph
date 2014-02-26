=======================
 Developing Hieroglyph
=======================

Hieroglyph uses Buildout_ to manage dependencies and development.

#. Check out the repository::

   $ git clone git@github.com:nyergler/hieroglyph.git

#. Bootstrap and run buildout::

   $ python bootstrap.py
   $ ./bin/buildout

After running Buildout, you can run ``./bin/python`` to execute an
interpreter with Hieroglyph and its dependencies installed.

Running Tests
=============

The unit tests can be run via ``setup.py``::

  $ ./bin/python setup.py test

Tox_ can be used to run the tests with both Python 2.7 and 3.3. The
Tox configuration will run the tests with Sphinx 1.1.3, Sphinx 1.2,
and the development branch.

.. _Buildout: https://pypi.python.org/pypi/zc.buildout/2.2.1
.. _Tox: http://tox.readthedocs.org/en/latest/
