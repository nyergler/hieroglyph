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

Tox_ can be used to run the tests with both Python 2 and 3. The Tox
configuration will run the tests with Sphinx 1.1.x, Sphinx 1.2.x, and
the development branch. Note that Hieroglyph requires Tox 1.8.

::

  $ tox

Jasmine Tests for Javascript
----------------------------

There are some Jasmine_ tests in ``src/jstests`` that test theme
Javascript functionality. You can open ``src/jstests/SpecRunner.html``
in your browser to run those. Alternately, you can install the
``jasmine`` gem to do so.

If you have Bundler_ installed, get started by installing the
necessary gems::

  $ bundle install

Then run the tests using ``rake``::

  $ rake jasmine:ci JASMINE_CONFIG_PATH=./src/jstests/jasmine.yml

.. _Buildout: https://pypi.python.org/pypi/zc.buildout/2.2.1
.. _Tox: http://tox.readthedocs.org/en/latest/
.. _Jasmine: http://jasmine.github.io/
.. _Bundler: http://bundler.io/
