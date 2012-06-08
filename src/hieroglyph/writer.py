"""Writer Support for Hieroglyph Slides."""

from docutils import nodes
from sphinx.locale import _
from docutils.writers.html4css1 import HTMLTranslator as BaseTranslator
from sphinx.writers.html import HTMLTranslator

from hieroglyph import html


def depart_title(self, node):

    # XXX Because we want to inject our link into the title, this is
    # largely copy-pasta'd from sphinx.html.writers.HtmlTranslator.

    close_tag = self.context[-1]

    if (self.permalink_text and self.builder.add_permalinks and
        node.parent.hasattr('ids') and node.parent['ids']):
        aname = node.parent['ids'][0]

        if close_tag.startswith('</a></h'):
            self.body.append('</a>')

        self.body.append(u'<a class="headerlink" href="#%s" ' % aname +
                         u'title="%s">%s</a>' % (
                         _('Permalink to this headline'),
                         self.permalink_text))

        self.body.append(u'<a class="headerlink" href="%s#%s" ' % (
                                html.slide_path(self.builder), aname,) +
                         u'title="%s">%s' % (
                         _('Slides'),
                         self.builder.app.config.slide_html_slide_link_symbol))

        if not close_tag.startswith('</a></h'):
            self.body.append('</a>')

    BaseTranslator.depart_title(self, node)


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

    def depart_title(self, node):

        if node.parent.hasattr('ids') and node.parent['ids']:
            aname = node.parent['ids'][0]

            if self.builder.app.config.slide_link_to_html:
                self.body.append(u'<a class="headerlink" href="%s#%s" ' % (
                                        html.html_path(self.builder), aname,) +
                                 u'title="%s">%s</a>' % (
                                 _('View HTML'),
                                 self.builder.app.config.slide_html_slide_link_symbol))

        HTMLTranslator.depart_title(self, node)
