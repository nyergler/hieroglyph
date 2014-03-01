from unittest import TestCase

from bs4 import BeautifulSoup
from mock import MagicMock

from docutils import nodes

from hieroglyph.tests.util import (
    make_document,
    with_sphinx,
    TestApp,
)
from hieroglyph.tests import util

from hieroglyph.builder import SlideBuilder
from hieroglyph import directives


class SlideConfTests(TestCase):

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

        document = make_document(
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

    def test_slide(self):

        test_content = """
.. slide:: Heading

   Blarf
"""

        document = make_document(
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

        document = make_document(
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

        document = make_document(
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

    def test_builder_collision(self):

        html_sphinx = TestApp(
            buildername='slides',
            srcdir=util.test_root,
        )
        slides_sphinx = TestApp(
            buildername='html',
            srcdir=util.test_root,
        )
        self.assertEqual(html_sphinx.doctreedir, slides_sphinx.doctreedir)

        try:
            html_sphinx.build()
            slides_sphinx.build()

            with open(html_sphinx.builddir/'html'/'split_slides.html') as html_file:
                with open(slides_sphinx.builddir/'slides'/'split_slides.html') as slide_file:

                    html = BeautifulSoup(html_file.read())
                    slides = BeautifulSoup(slide_file.read())

                    self.assertEqual(
                        len(html.find_all('h2')),
                        1,
                    )
                    self.assertEqual(
                        len(slides.find_all('h2')),
                        3,
                    )

        finally:
            html_sphinx.cleanup()
            slides_sphinx.cleanup()


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
    def test_copied_title(self, sphinx_app):

        sphinx_app.build()

        with open(
            sphinx_app.builddir/'slides'/'split_slides.html'
        ) as html_file:

            slide_html = BeautifulSoup(
                html_file.read()
            )
            slides = slide_html.find_all('article', class_='slide')[1:]
            first_title = slides[0].find('h2').text

            for idx, slide in enumerate(slides[1:]):
                title = slide.find('h2').text
                self.assertEqual(
                    title,
                    first_title,
                )

    @with_sphinx(
        buildername='slides',
        srcdir=util.test_root,
    )
    def test_increment_slide_title(self, sphinx_app):

        sphinx_app.build()

        with open(
            sphinx_app.builddir/'slides'/'split_slides_increment.html'
        ) as html_file:

            slide_html = BeautifulSoup(
                html_file.read()
            )
            slides = slide_html.find_all('article', class_='slide')[1:]
            first_title = slides[0].find('h2').text

            for idx, slide in enumerate(slides[1:]):
                title = slide.find('h2').text
                self.assertEqual(
                    title,
                    '%s (%d)' % (first_title, idx+2),
                )


class TransformNextSlideTests(TestCase):

    def setUp(self):

        self.app = TestApp(buildername='slides')
        self.builder = SlideBuilder(self.app)
        self.document = make_document(
            'testing',
            """\
Slide Title
-----------

* Bullet 1
* Bullet 2

.. nextslide::

Additional Text

""",
        )
        self.builder.init_templates()

    def test_visit_slide_creates_new_slide_data(self):

        self.assertEqual(
            len(self.document.traverse(nodes.section)),
            1,
        )

        transformer = directives.TransformNextSlides(self.document)
        transformer.apply_to_document(
            self.document,
            env=MagicMock(),
            building_slides=False,
        )

        self.assertEqual(
            len(self.document.traverse(nodes.section)),
            1,
        )
