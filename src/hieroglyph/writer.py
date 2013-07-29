"""Writer Support for Hieroglyph Slides."""

from docutils import nodes
from sphinx.locale import _
from docutils.writers.html4css1 import HTMLTranslator as BaseTranslator
from sphinx.writers.html import HTMLTranslator

from hieroglyph import html
from hieroglyph.directives import (
    slide,
    slideconf,
)


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

        self.body.append(
            u'<a class="headerlink" href="%s#%s" ' % (
                html.slide_path(self.builder),
                aname,
            ) +
            u'title="%s">%s' % (
                _('Slides'),
                self.builder.app.config.slide_html_slide_link_symbol,
            ))

        if not close_tag.startswith('</a></h'):
            self.body.append('</a>')

    BaseTranslator.depart_title(self, node)


class BaseSlideTranslator(HTMLTranslator):

    def __init__(self, *args, **kwargs):

        HTMLTranslator.__init__(self, *args, **kwargs)

        self.section_count = 0

    def visit_slideconf(self, node):
        pass

    def depart_slideconf(self, node):
        pass

    def _add_slide_number(self, slide_no):
        """Add the slide number to the output if enabled."""

        if self.builder.config.slide_numbers:
            self.body.append(
                '\n<div class="slide-no">%s</div>\n' % (slide_no,),
            )

    def visit_slide(self, node):

        from hieroglyph import builder

        slide_level = node.attributes.get('level', self.section_level)

        if slide_level > self.builder.config.slide_levels:
            # dummy for matching div's
            self.body.append(
                self.starttag(
                    node, 'div', CLASS='section level-%s' % slide_level)
            )
            node.tag_name = 'div'
        else:
            slide_conf = slideconf.get_conf(self.builder, node.document)
            if (builder.building_slides(self.builder.app) and
                    slide_conf['autoslides'] and
                    isinstance(node.parent, nodes.section) and
                    not getattr(node.parent, 'closed', False)):

                # we're building slides and creating slides from
                # sections; close the previous section, if needed
                self.depart_slide(node.parent)

            # don't increment section_count until we've (potentially)
            # closed the previous slide
            self.section_count += 1

            node.closed = False

            classes = []
            if not node.get('classes'):
                classes = slide_conf['slide_classes']

            self.body.append(
                self.starttag(
                    node, 'article',
                    CLASS='%s slide level-%s' % (
                        ' '.join(classes),
                        slide_level,
                    ),
                )
            )
            node.tag_name = 'article'

    def depart_slide(self, node):

        if not getattr(node, 'closed', False):

            # mark the slide closed
            node.closed = True

            self._add_slide_number(self.section_count)
            self.body.append(
                '\n</%s>\n' % getattr(node, 'tag_name', 'article')
            )

    def visit_title(self, node):

        if (isinstance(node.parent, slide) or
                node.parent.attributes.get('include-as-slide', False)):
            slide_level = node.parent.attributes.get(
                'level',
                self.section_level)
            level = max(
                slide_level + self.initial_header_level - 1,
                1,
            )

            tag = 'h%s' % level
            self.body.append(self.starttag(node, tag, ''))
            self.context.append('</%s>\n' % tag)
        else:
            HTMLTranslator.visit_title(self, node)


class SlideTranslator(BaseSlideTranslator):

    def visit_section(self, node):

        # XXX: We're actually removing content that's not in slide
        # nodes with autoslides is false, so it's not clear that we
        # even need this guard.
        if (slideconf.get_conf(self.builder, node.document)['autoslides'] or
                node.attributes.get('include-as-slide', False)):

            self.section_level += 1
            return self.visit_slide(node)

    def depart_section(self, node):

        if (slideconf.get_conf(self.builder, node.document)['autoslides'] or
                node.attributes.get('include-as-slide', False)):

            if self.section_level > self.builder.config.slide_levels:
                self.body.append('</div>')
            else:
                self.depart_slide(node)

            self.section_level -= 1

    def depart_title(self, node):

        if node.parent.hasattr('ids') and node.parent['ids']:
            aname = node.parent['ids'][0]

            if self.builder.app.config.slide_link_to_html:
                self.body.append(
                    u'<a class="headerlink" href="%s#%s" ' % (
                        html.html_path(self.builder),
                        aname,
                    ) +
                    u'title="%s">%s</a>' % (
                        _('View HTML'),
                        self.builder.app.config.slide_html_slide_link_symbol,
                    ))

        HTMLTranslator.depart_title(self, node)
