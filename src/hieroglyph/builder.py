import os.path

from docutils import nodes
from sphinx.theming import Theme
from sphinx.builders.html import (
    StandaloneHTMLBuilder,
    DirectoryHTMLBuilder,
)
from sphinx.util import copy_static_entry

from hieroglyph import writer
from hieroglyph import directives

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
        """Return the configured theme name and options."""

        return self.config.slide_theme, self.config.slide_theme_options

    def init_templates(self):
        Theme.init_themes(self.confdir,
                          self.get_builtin_theme_dirs() + self.config.slide_theme_path,
                          warn=self.warn)
        themename, themeoptions = self.get_theme_config()

        self.create_template_bridge()

        self._theme_stack = []
        self._additional_themes = []

        self.theme = self.theme_options = None
        self.apply_theme(themename, themeoptions)

    def apply_theme(self, themename, themeoptions):

        # push the existing values onto the Stack
        self._theme_stack.append(
            (self.theme, self.theme_options)
        )

        self.theme = Theme(themename)
        self.theme_options = themeoptions.copy()
        self.templates.init(self, self.theme)

        self._additional_themes.append(self.theme)

    def pop_theme(self):

        self.theme, self.theme_options = self._theme_stack.pop()

        self.templates.init(self, self.theme)

    def get_doc_context(self, docname, body, metatags):

        context = super(AbstractSlideBuilder, self).get_doc_context(
            docname, body, metatags,
        )

        if self.theme:
            context.update(dict(
                style = self.theme.get_confstr('theme', 'stylesheet'),
            ))

        return context

    def write_doc(self, docname, doctree):

        slideconf = doctree.traverse(directives.slideconf)
        if slideconf:
            slideconf = slideconf[-1]
            slideconf.apply(self)

        result = super(AbstractSlideBuilder, self).write_doc(docname, doctree)

        if slideconf:
            # restore the previous theme configuration
            slideconf.restore(self)

    def post_process_images(self, doctree):
        """Pick the best candidate for all image URIs."""

        super(AbstractSlideBuilder, self).post_process_images(doctree)

        for node in doctree.traverse(nodes.image):

            if node.get('candidates') is None:
                node['candidates'] = ('*',)

            # fix up images with absolute paths
            if node['uri'].startswith(self.outdir):
                node['uri'] = node['uri'][len(self.outdir) + 1:]

    def copy_static_files(self):

        result = super(AbstractSlideBuilder, self).copy_static_files()

        # add context items for search function used in searchtools.js_t
        ctx = self.globalcontext.copy()
        ctx.update(self.indexer.context_for_searchtool())

        for theme in self._additional_themes:

            themeentries = [os.path.join(themepath, 'static')
                            for themepath in theme.get_dirchain()[::-1]]
            for entry in themeentries:
                copy_static_entry(entry, os.path.join(self.outdir, '_static'),
                                  self, ctx)

        return result


class DirectorySlideBuilder(AbstractSlideBuilder, DirectoryHTMLBuilder):

    name = 'dirslides'


class SlideBuilder(AbstractSlideBuilder, StandaloneHTMLBuilder):

    name = 'slides'
