from docutils import nodes

from sphinx.util.nodes import set_source_info
from docutils.parsers.rst import Directive, directives


class slides(nodes.Element): pass


class Slides(Directive):

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}

    def run(self):
        node = slides()
        node.document = self.state.document
        set_source_info(self, node)

        node.slides = self.name == 'slides'

        self.state.nested_parse(self.content, self.content_offset,
                                node, match_titles=1)
        return [node]


def process_slide_nodes(app, doctree, docname):

    from hieroglyph import builder

    is_slides = builder.building_slides(app)

    # this is a slide builder, remove notslides nodes
    for node in doctree.traverse(slides):

        keep_content = is_slides == node.slides

        if keep_content:
            node.replace_self(node.children)
        else:
            node.replace_self([])


class slideconf(nodes.Element):

    def apply(self, builder):
        """Apply the Slide Configuration to a Builder."""

        if 'theme' in self.attributes:
            builder.apply_theme(
                self.attributes['theme'],
                builder.theme_options,
            )

    def restore(self, builder):
        """Restore the previous Slide Configuration for the Builder."""

        builder.pop_theme()

class SlideConf(Directive):

    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'theme': directives.unchanged,
    }

    def run(self):
        node = slideconf(**self.options)
        node.document = self.state.document
        set_source_info(self, node)

        return [node]


def process_slideconf_nodes(app, doctree, docname):

    from hieroglyph import builder

    is_slides = builder.building_slides(app)

    if is_slides:
        return

    # if we're not building slides, remove slideconf
    for node in doctree.traverse(slideconf):

        node.replace_self([])
