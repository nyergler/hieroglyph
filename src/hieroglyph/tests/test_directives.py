from unittest import TestCase

from bs4 import BeautifulSoup

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


class TestSlideConditions(TestCase):

    @with_sphinx(
        buildername='html',
        srcdir=util.test_root,
    )
    def test_slide_content_removed_when_building_html(self, sphinx_app):

        sphinx_app.build()

        with open(sphinx_app.builddir/'html'/'index.html') as html_file:
            html = html_file.read()

            self.assertIn('OTHERBUILDERS', html)
            self.assertNotIn('SLIDES', html)

    @with_sphinx(
        buildername='slides',
        srcdir=util.test_root,
    )
    def test_notslide_content_removed_when_building_slides(self, sphinx_app):

        sphinx_app.build()

        with open(sphinx_app.builddir/'slides'/'index.html') as html_file:
            html = html_file.read()

            self.assertIn('SLIDES', html)
            self.assertNotIn('OTHERBUILDERS', html)

    @with_sphinx(
        buildername='html',
        srcdir=util.test_root,
    )
    def test_sections_in_cond_nodes_appear_in_toc(self, sphinx_app):
        sphinx_app.build()

        with open(sphinx_app.builddir/'html'/'index.html') as html_file:
            tree = BeautifulSoup(html_file.read())
            contents = tree.find(
                'div',
                attrs=dict(id='contents'),
            )
            self.assertEqual(
                len(contents.find_all('li')),
                2,
            )


class NextSlideTests(TestCase):

    @with_sphinx(
        buildername='slides',
        srcdir=util.test_root,
    )
    def test_nextslide_splits_content(self, sphinx_app):

        sphinx_app.build()

        with open(
            sphinx_app.builddir/'slides'/'split_slide_title_override.html'
        ) as html_file:

            slide_html = BeautifulSoup(
                html_file.read()
            )
            slides = slide_html.find_all('article', class_='slide')

            # There are only two sections in the document; two
            # nextslide directives split the final section into 3
            self.assertEqual(
                len(slides),
                4,
            )

            self.assertEqual(
                slides[2].find('h2').text,
                'B Section',
            )

            self.assertEqual(
                slides[3].find('h2').text,
                'C Section',
            )

    @with_sphinx(
        buildername='slides',
        srcdir=util.test_root,
    )
    def test_autogenerated_title(self, sphinx_app):

        sphinx_app.build()

        with open(
            sphinx_app.builddir/'slides'/'split_slides.html'
        ) as html_file:

            slide_html = BeautifulSoup(
                html_file.read()
            )
            slides = slide_html.find_all('article', class_='slide')[1:]
            first_title = slides[0].find('h2').text

            for slide in slides[1:]:
                title = slide.find('h2').text
                self.assertTrue(
                    title.startswith(first_title),
                    msg='Slide title (%s) does not begin wth correct text (%s).' % (
                        title,
                        first_title,
                    ),
                )
