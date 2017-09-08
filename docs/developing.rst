=======================
 Developing Hieroglyph
=======================

Running Tests
=============

The unit tests can be run via ``setup.py``::

  $ ./bin/python setup.py test

Tox_ can be used to run the tests with both Python 2 and 3. The Tox
configuration will run the tests with Sphinx 1.4, Sphinx 1.5, Sphinx 1.6, and
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

Releasing
=========

Hieroglyph uses `Versioneer`_ to manage version numbers in releases. Versioneer
derives the version number from the latest tag and source information.

To make a release, use the following steps.

1. Update ``NEWS.txt`` to include the release date and information.
#. Tag the release with git::

    $ git tag hieroglyph-x.y.z

#. Build the distributions::

    $ python setup.py sdist bdist_wheel

#. Upload the distributions to PyPI; the recommended tool for this is Twine_.
   ::

    $ twine upload dist/*

.. _Buildout: https://pypi.python.org/pypi/zc.buildout/2.2.1
.. _Tox: http://tox.readthedocs.org/en/latest/
.. _Jasmine: http://jasmine.github.io/
.. _Bundler: http://bundler.io/
.. _Versioneer: https://github.com/warner/python-versioneer
.. _Twine: https://pypi.python.org/pypi/twine