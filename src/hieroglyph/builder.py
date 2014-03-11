"""Available slide building classes."""

import json
import os

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

    format = 'slides'
    add_permalinks = False

    def init_translator_class(self):
        self.translator_class = writer.SlideTranslator

    def get_builtin_theme_dirs(self):

        return [
            os.path.join(os.path.dirname(__file__), 'themes',)
        ]

    def get_theme_config(self):
        """Return the configured theme name and options."""

        return self.config.slide_theme, self.config.slide_theme_options

    def get_theme_options(self):
        """Return a dict of theme options, combining defaults and overrides."""

        overrides = self.get_theme_config()[1]
        return self.theme.get_options(overrides)

    def init_templates(self):
        Theme.init_themes(self.confdir,
                          self.get_builtin_theme_dirs() +
                          self.config.slide_theme_path,
                          warn=self.warn)
        themename, themeoptions = self.get_theme_config()

        self.create_template_bridge()
        self._theme_stack = []
        self._additional_themes = []

        self.theme = self.theme_options = None
        self.apply_theme(themename, themeoptions)

    def apply_theme(self, themename, themeoptions):
        """Apply a new theme to the document.

        This will store the existing theme configuration and apply a new one.

        """

        # push the existing values onto the Stack
        self._theme_stack.append(
            (self.theme, self.theme_options)
        )

        self.theme = Theme(themename)
        self.theme_options = themeoptions.copy()
        self.templates.init(self, self.theme)
        self.templates.environment.filters['json'] = json.dumps

        if self.theme not in self._additional_themes:
            self._additional_themes.append(self.theme)

    def pop_theme(self):
        """Disable the most recent theme, and restore its predecessor."""

        self.theme, self.theme_options = self._theme_stack.pop()

    def prepare_writing(self, docnames):

        super(AbstractSlideBuilder, self).prepare_writing(docnames)

        # override items in the global context if needed
        if self.config.slide_title:
            self.globalcontext['docstitle'] = self.config.slide_title

    def get_doc_context(self, docname, body, metatags):

        context = super(AbstractSlideBuilder, self).get_doc_context(
            docname, body, metatags,
        )

        if self.theme:
            context.update(dict(
                style=self.theme.get_confstr('theme', 'stylesheet'),
            ))

        return context

    def write_doc(self, docname, doctree):

        slideconf = directives.slideconf.get(doctree)
        if slideconf:
            slideconf.apply(self)

        result = super(AbstractSlideBuilder, self).write_doc(docname, doctree)

        if slideconf:
            # restore the previous theme configuration
            slideconf.restore(self)

        return result

    def post_process_images(self, doctree):
        """Pick the best candidate for all image URIs."""

        super(AbstractSlideBuilder, self).post_process_images(doctree)

        # figure out where this doctree is in relation to the srcdir
        relative_base = (
            ['..'] *
            doctree.attributes.get('source')[len(self.srcdir) + 1:].count('/')
        )

        for node in doctree.traverse(nodes.image):

            if node.get('candidates') is None:
                node['candidates'] = ('*',)

            # fix up images with absolute paths
            if node['uri'].startswith(self.outdir):
                node['uri'] = '/'.join(
                    relative_base + [
                        node['uri'][len(self.outdir) + 1:]
                    ]
                )

    def copy_static_files(self):

        result = super(AbstractSlideBuilder, self).copy_static_files()

        # add context items for search function used in searchtools.js_t
        ctx = self.globalcontext.copy()
        ctx.update(self.indexer.context_for_searchtool())

        for theme in self._additional_themes[1:]:

            themeentries = [os.path.join(themepath, 'static')
                            for themepath in theme.get_dirchain()[::-1]]
            for entry in themeentries:
                copy_static_entry(entry, os.path.join(self.outdir, '_static'),
                                  self, ctx)

        return result


class DirectorySlideBuilder(AbstractSlideBuilder, DirectoryHTMLBuilder):
    """This is the standard Directory Slide HTML builder.

    Its output is a directory with HTML files, where each file is
    called ``index.html`` and placed in a subdirectory named like its
    page name. For example, the document ``markup/rest.rst`` will not
    result in an output file ``markup/rest.html``, but
    ``markup/rest/index.html``. When generating links between pages,
    the ``index.html`` is omitted, so that the URL would look like
    ``markup/rest/``.

    The output directry will include any needed style sheets, slide
    table, and presenter's console JavaScript.

    Its name is ``dirslides``.

    """

    name = 'dirslides'


class SlideBuilder(AbstractSlideBuilder, StandaloneHTMLBuilder):
    """This is the standard Slide HTML builder.

    Its output is a directory with HTML, along with the needed style
    sheets, slide table, and presenter's console JavaScript.

    Its name is ``slides``.

    """

    name = 'slides'


class AbstractInlineSlideBuilder(object):

    name = 'inlineslides'

    def __init__(self, *args, **kwargs):
        super(AbstractInlineSlideBuilder, self).__init__(*args, **kwargs)

        self.config.html_static_path.append(
            os.path.relpath(
                os.path.join(
                    os.path.dirname(__file__),
                    'themes',
                    'inline-slides',
                    'static',
                ),
                self.confdir,
            )
        )

        self.css_files.append('_static/slides.css')

    def init_translator_class(self):
        self.translator_class = writer.BaseSlideTranslator


class DirectoryInlineSlideBuilder(
        AbstractInlineSlideBuilder,
        DirectoryHTMLBuilder):
    """This is the Inline Slide Directory HTML builder.

    The inline slide builder add support for the ``slide`` directive
    to Sphinx's :py:class:`DirectoryHTMLBuilder`, and adds an
    additional stylesheet to the output for basic inline display.

    When using an inline builder :confval:`autoslides` is disabled.

    Its name is ``dirinlineslides``.

    .. versionadded:: 0.5

    """

    name = 'dirinlineslides'


class InlineSlideBuilder(AbstractInlineSlideBuilder, StandaloneHTMLBuilder):
    """This is the Inline Slide HTML builder.

    The inline slide builder add support for the ``slide`` directive
    to Sphinx's :py:class:`StandaloneHTMLBuilder`, and adds an
    additional stylesheet to the output for basic inline display.

    When using an inline builder :confval:`autoslides` is disabled.

    Its name is ``inlineslides``.

    .. versionadded:: 0.5

    """

    name = 'inlineslides'
