from unittest import TestCase

from hieroglyph.tests.util import (
    with_sphinx,
    TestApp,
)
import hieroglyph.builder


class SlideBuilderTests(TestCase):

    def test_get_theme_options(self):

        app = TestApp()
        builder = hieroglyph.builder.SlideBuilder(app)

        resolved_theme_options = builder.get_theme_options()
        self.assertIsInstance(
            resolved_theme_options,
            dict,
        )

        self.assertIn(
            'custom_css',
            resolved_theme_options,
        )
        self.assertIn(
            'custom_js',
            resolved_theme_options,
        )

    def test_get_theme_options_with_overrides(self):

        app = TestApp()
        builder = hieroglyph.builder.SlideBuilder(app)
        resolved_theme_options = builder.get_theme_options()

        self.assertEqual(
            resolved_theme_options['custom_css'],
            '',
        )

        app = TestApp(
            confoverrides={
                'slide_theme_options': {
                    'custom_css': 'testing.css',
                },
            },
        )
        builder = hieroglyph.builder.SlideBuilder(app)
        resolved_theme_options = builder.get_theme_options()

        self.assertEqual(
            resolved_theme_options['custom_css'],
            'testing.css',
        )

    @with_sphinx(
        buildername='slides',
    )
    def test_html_static_dir_contents_override_theme(self, sphinx_app):

        self.assertIsInstance(
            sphinx_app.builder,
            hieroglyph.builder.AbstractSlideBuilder,
        )

        sphinx_app.build()

        built_styles = open(sphinx_app.builddir/'slides'/'_static'/'styles.css').read()
        static_styles = open(sphinx_app.srcdir/'_static'/'styles.css').read()

        self.assertEqual(
            built_styles,
            static_styles,
        )

    def test_docstitle_uses_slidetitle(self):

        app = TestApp(
            confoverrides={
                'slide_title': 'SLIDES TITLE',
            },
        )
        builder = hieroglyph.builder.SlideBuilder(app)

        builder.prepare_writing([])

        self.assertEqual(
            builder.globalcontext['docstitle'],
            'SLIDES TITLE',
        )

    def test_docstitle_fallback_to_html_title(self):

        app = TestApp()
        builder = hieroglyph.builder.SlideBuilder(app)

        builder.prepare_writing([])

        self.assertEqual(
            builder.globalcontext['docstitle'],
            builder.config.html_title,
        )
