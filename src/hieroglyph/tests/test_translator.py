from unittest import TestCase

from docutils import nodes
from mock import patch
from sphinx import jinja2glue

from hieroglyph.tests.util import (
    TestApp,
    make_document,
)
from hieroglyph.builder import SlideBuilder
from hieroglyph.writer import (
    SlideData,
    BaseSlideTranslator,
    SlideTranslator,
)


class SlideTranslationTests(TestCase):

    def setUp(self):

        self.app = TestApp(buildername='slides')
        self.builder = SlideBuilder(self.app)
        self.document = make_document(
            'testing',
            """\
Slide ``Title``
---------------

* Bullet 1
* Bullet 2

""",
        )
        self.translator = BaseSlideTranslator(
            self.builder,
            self.document,
        )
        self.builder.init_templates()

    def test_push_body(self):

        self.translator.body = [1, 2, 3]

        self.translator.push_body()

        self.assertEqual(self.translator.body, [])
        self.assertEqual(self.translator.body_stack, [[1, 2, 3]])

        self.translator.body.append('foo')
        self.translator.push_body()
        self.assertEqual(
            self.translator.body_stack,
            [
                [1, 2, 3, ],
                ['foo', ],
            ],
        )

    def test_pop_body(self):

        self.translator.body.append('a')
        self.translator.push_body()

        self.translator.body.append('1')
        self.translator.push_body()

        self.assertEqual(
            self.translator.body_stack,
            [
                ['a'],
                ['1'],
            ],
        )
        self.assertEqual(self.translator.body, [])

        self.translator.pop_body()
        self.assertEqual(
            self.translator.body_stack,
            [
                ['a'],
            ],
        )
        self.assertEqual(self.translator.body, ['1'])

    def test_visit_slide_creates_new_slide_data(self):

        # sanity checks
        self.assertIsNone(self.translator.current_slide)
        self.assertIsInstance(self.document[0], nodes.section)

        # visit the slide section
        self.translator.visit_slide(self.document[0])

        # verify the Slide was created
        self.assertIsNotNone(self.translator.current_slide)
        self.assertIsInstance(self.translator.current_slide, SlideData)
        self.assertEqual(
            self.translator.current_slide.level,
            self.document[0].attributes.get(
                'level',
                self.translator.section_level,
            ),
        )

    def test_section_classes_added_to_slidedata(self):

        self.document[0].set_class('fancy')

        # visit the slide section
        self.translator.visit_slide(self.document[0])

        self.assertEqual(
            self.translator.current_slide.classes,
            ['fancy'],
        )

    def test_depart_slide_clears_current_slide(self):

        # visit the slide section
        self.translator.visit_slide(self.document[0])
        self.assertIsNotNone(self.translator.current_slide)

        self.translator.depart_slide(self.document[0])
        self.assertIsNone(self.translator.current_slide)

    def test_visit_title_in_slide_sets_slide_title(self):

        # visit the slide section
        self.translator.visit_slide(self.document[0])

        # visit the title
        self.translator.visit_title(self.document[0][0])

        self.assertEqual(
            self.document[0][0].astext(),
            self.translator.current_slide.title,
        )

    def test_depart_slide_sets_slide_content(self):
        pass

    def test_slide_data_get_context(self):

        slide = SlideData(
            self.translator,
            title='My Pretty Slide',
            id='my-pretty-slide',
            level=1,
        )

        self.assertEqual(
            slide.get_slide_context(),
            {
                'title': 'My Pretty Slide',
                'level': 1,
                'content': '',
                'classes': [],
                'id': 'my-pretty-slide',
                'slide_number': 0,
                'config': self.translator.builder.config,
            },
        )

    @patch.object(jinja2glue.BuiltinTemplateLoader, 'render')
    def test_depart_slide_calls_template_render(self, render_mock):

        self.translator.visit_slide(self.document[0])
        self.assertIsNotNone(self.translator.current_slide)
        current_slide = self.translator.current_slide

        self.translator.depart_slide(self.document[0])
        self.assertIsNone(self.translator.current_slide)

        render_mock.assert_called_once_with(
            'slide.html',
            current_slide.get_slide_context(),
        )

    @patch.object(
        jinja2glue.BuiltinTemplateLoader,
        'render',
        return_value='** SLIDE **',
    )
    def test_rendered_template_added_to_body(self, render_mock):

        self.translator.visit_slide(self.document[0])
        self.translator.depart_slide(self.document[0])

        self.assertIsNone(self.translator.current_slide)
        self.assertEqual(
            self.translator.body[-1],
            '** SLIDE **',
        )

    @patch.object(
        jinja2glue.BuiltinTemplateLoader,
        'render',
        return_value='** SLIDE **',
    )
    def test_only_rendered_template_added(self, render_mock):

        self.translator.visit_section = self.translator.visit_slide
        self.translator.depart_section = self.translator.depart_slide
        self.document.walkabout(self.translator)

        self.assertEqual(
            self.translator.body,
            ['** SLIDE **'],
        )

    def test_section_id_added_to_current_slide(self):
        self.document[0].set_class('fancy')

        # visit the slide section
        self.translator.visit_slide(self.document[0])

        self.assertEqual(
            self.translator.current_slide.id,
            'slide-title',
        )

    def test_inline_markup_in_title(self):

        self.translator.visit_section = self.translator.visit_slide
        self.translator.depart_section = self.translator.depart_slide
        self.document.walkabout(self.translator)

        self.assertEqual(
            self.translator.slide_data[-1].title,
            'Slide <tt class="docutils literal">'
            '<span class="pre">Title</span></tt>',
        )

    def test_non_section_titles_rendered_normally(self):
        document = make_document(
            'testing',
            """\
Section Title
-------------

Some Text

.. note:: Take note!

Another paragraph

""",
        )
        translator = SlideTranslator(
            self.builder,
            document,
        )

        document.walkabout(translator)

        self.assertEqual(
            translator.body,
            [
                u'\n<article class="slide level-1" id="section-title">\n\n'
                '<h1>Section Title</h1>\n\n'
                '<p>Some Text</p>\n'
                '<div class="admonition note">\n'
                '<p class="first admonition-title">Note</p>\n'
                '<p class="last">Take note!</p>\n'
                '</div>\n'
                '<p>Another paragraph</p>'
                '\n\n\n\n\n</article>',
            ],
        )

    def test_slide_titles(self):
        document = make_document(
            'testing',
            """\
.. slide:: Slide Title

   Slide Content

""",
        )
        translator = SlideTranslator(
            self.builder,
            document,
        )

        document.walkabout(translator)

        self.assertEqual(
            translator.body,
            [
                u'\n<article class="admonition-slide-title slide level-1">\n\n'
                '<h1>Slide Title</h1>\n\n'
                '<p>Slide Content</p>\n\n\n\n\n</article>',
            ],
        )
