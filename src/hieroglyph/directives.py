from docutils import nodes

from sphinx.util.nodes import set_source_info
from sphinx.util.compat import Directive

from hieroglyph import builder


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

    is_slides = isinstance(app.builder, builder.AbstractSlideBuilder)

    # this is a slide builder, remove notslides nodes
    for node in doctree.traverse(slides):

        keep_content = is_slides == node.slides

        if keep_content:
            node.replace_self(node.children)
        else:
            node.replace_self([])
