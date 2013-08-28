from unittest import TestCase

import docutils.frontend
import docutils.parsers.rst
import docutils.utils

from hieroglyph.tests.util import with_sphinx
from hieroglyph.tests import util

from hieroglyph import directives


class SlideConfTests(TestCase):

    def _make_document(self, source, contents):

        parser = docutils.parsers.rst.Parser()
        document = docutils.utils.new_document(
            source,
            docutils.frontend.OptionParser(
                components=(docutils.parsers.rst.Parser,)
            ).get_default_values(),
        )

        parser.parse(contents, document)

        return document

    @with_sphinx()
    def test_filter_doctree(self, sphinx_app):
        """Only slide related elements will be retained when filtering."""

        test_content = """

.. slideconf::
   :autoslides: False

Heading
=======

.. slide:: Heading

   Blarf

Second Level
------------

* Point 1
* Point 2

"""

        document = self._make_document(
            'slideconf_test',
            test_content,
        )

        directives.filter_doctree_for_slides(document)

        # only two elements remain -- the slideconf and slide element
        self.assertEqual(len(document.children), 2)

    @with_sphinx(
        buildername='slides',
        srcdir=util.test_root.parent/'no-autoslides',
    )
    def test_trailing_content_removed(self, sphinx_app):

        sphinx_app.build()

        self.assertFalse(
            'TESTING_SENTINEL' in
            open(sphinx_app.builddir/'slides'/'index.html').read(),
            'The sentinel paragraph should have been filtered.',
        )


class SlideTests(TestCase):

    def _make_document(self, source, contents):

        parser = docutils.parsers.rst.Parser()
        document = docutils.utils.new_document(
            source,
            docutils.frontend.OptionParser(
                components=(docutils.parsers.rst.Parser,)
            ).get_default_values(),
        )

        parser.parse(contents, document)

        return document

    def test_slide(self):

        test_content = """
.. slide:: Heading

   Blarf
"""

        document = self._make_document(
            'slide_directive_test',
            test_content,
        )

        self.assertEqual(
            document[0][0][0].title(),
            u'Heading',
        )

        self.assertEqual(
            document[0][1][0].title(),
            u'Blarf',
        )

    def test_slide_without_content(self):

        test_content = """
.. slide:: Heading

Another Paragraph
"""

        document = self._make_document(
            'slide_directive_test',
            test_content,
        )

        self.assertEqual(
            document[0].tagname,
            'slide',
        )
        self.assertEqual(len(document[0]), 1)

        self.assertEqual(
            document[1].tagname,
            'paragraph',
        )

    def test_slide_without_title(self):


        test_content = """
.. slide::

   Only Content Here

Another Paragraph
"""

        document = self._make_document(
            'slide_directive_test',
            test_content,
        )

        self.assertEqual(
            document[0].tagname,
            'slide',
        )
        self.assertEqual(len(document[0]), 1)

        self.assertEqual(
            document[1].tagname,
            'paragraph',
        )
