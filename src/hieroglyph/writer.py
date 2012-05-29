"""Writer Support for Hieroglyph Slides."""

from docutils import nodes
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

    def visit_title(self, node):
        if isinstance(node.parent, nodes.section):
            level = self.section_level + self.initial_header_level - 1

            tag = 'h%s' % level
            self.body.append(self.starttag(node, tag, ''))
            self.context.append('</%s>\n' % tag)
        else:
            HTMLTranslator.visit_subtitle(self, node)
