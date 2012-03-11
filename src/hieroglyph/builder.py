import os.path

from docutils import nodes
from sphinx.theming import Theme
from sphinx.builders.html import DirectoryHTMLBuilder
from sphinx.writers.html import HTMLTranslator


class SlideTranslator(HTMLTranslator):

    def __init__(self, *args, **kwargs):

        HTMLTranslator.__init__(self, *args, **kwargs)

        self.section_count = 0

    def visit_section(self, node):

        self.section_count += 1
        self.section_level += 1

        if self.section_level > self.builder.config.slide_levels:
            # dummy for matching div's
            self.body.append(
                self.starttag(
                    node, 'div', CLASS='section level-%s' % self.section_level)
            )
        else:
            if self.section_level > 1 and not getattr(node.parent, 'closed', False):
                # close the previous slide
                node.parent.closed = True
                self.body.append('\n</article>\n')

            node.closed = False
            self.body.append(
                self.starttag(
                    node, 'article', CLASS='slide level-%s' % self.section_level))

    def depart_section(self, node):

        if self.section_level > self.builder.config.slide_levels:
            self.body.append('</div>')
        else:
            if not getattr(node, 'closed', False):
                self.body.append('</article>\n')

        self.section_level -= 1

    def visit_subtitle(self, node):
        if isinstance(node.parent, nodes.section):
            level = self.section_level + self.initial_header_level - 1
            if level == 1:
                level = 2
            tag = 'h%s' % level
            self.body.append(self.starttag(node, tag, ''))
            self.context.append('</%s>\n' % tag)
        else:
            html4css1.HTMLTranslator.visit_subtitle(self, node)


class SlideBuilder(DirectoryHTMLBuilder):

    name = 'html5slides'

    def init_translator_class(self):
        self.translator_class = SlideTranslator

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

        return super(SlideBuilder, self).post_process_images(doctree)


def setup(app):

    app.add_builder(SlideBuilder)

    app.add_config_value('slide_theme', 'slides', 'html')
    app.add_config_value('slide_levels', 3, 'html')
    app.add_config_value('slide_theme_options', {}, 'html')
    app.add_config_value('slide_theme_path', [], 'html')
