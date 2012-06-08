import os.path

from docutils import nodes
from sphinx.theming import Theme
from sphinx.builders.html import (
    StandaloneHTMLBuilder,
    DirectoryHTMLBuilder,
)

from hieroglyph import writer


def building_slides(app):
    """Returns True if building Slides."""

    return isinstance(app.builder, AbstractSlideBuilder)


class AbstractSlideBuilder(object):

    add_permalinks = False

    def init_translator_class(self):
        self.translator_class = writer.SlideTranslator

    def get_builtin_theme_dirs(self):

        return [os.path.join(
            os.path.dirname(__file__), 'themes',
            )]

    def get_theme_config(self):
        return self.config.slide_theme, self.config.slide_theme_options

    def init_templates(self):
        Theme.init_themes(self.confdir,
                          self.get_builtin_theme_dirs() + self.config.slide_theme_path,
                          warn=self.warn)
        themename, themeoptions = self.get_theme_config()
        self.theme = Theme(themename)
        self.theme_options = themeoptions.copy()
        self.create_template_bridge()
        self.templates.init(self, self.theme)

    def post_process_images(self, doctree):
        """Pick the best candidate for all image URIs."""

        for node in doctree.traverse(nodes.image):

            if node.get('candidates') is None:
                node['candidates'] = ('*',)

            # fix up images with absolute paths
            if node['uri'].startswith(self.outdir):
                node['uri'] = node['uri'][len(self.outdir) + 1:]

        return super(AbstractSlideBuilder, self).post_process_images(doctree)


class DirectorySlideBuilder(AbstractSlideBuilder, DirectoryHTMLBuilder):

    name = 'dirslides'


class SlideBuilder(AbstractSlideBuilder, StandaloneHTMLBuilder):

    name = 'slides'
