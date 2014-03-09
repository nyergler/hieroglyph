from unittest import TestCase

from hieroglyph.tests.util import TestApp
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
