from docutils import nodes

from sphinx.util.nodes import set_source_info
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives import (
    admonitions,
)
from docutils.parsers.rst.roles import set_classes


class slides(nodes.Element):
    pass


class IfBuildingSlides(Directive):

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


def process_slidecond_nodes(app, doctree, docname):

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


class slide(nodes.admonition):
    pass


class SlideDirective(admonitions.Admonition):

    node_class = slide
    option_spec = {
        'class': directives.class_option,
        'name': directives.unchanged,
        'level': directives.nonnegative_int,
    }

    def run(self):

        # largely lifted from the superclass in order to make titles work
        set_classes(self.options)
        self.assert_has_content()
        text = '\n'.join(self.content)
        admonition_node = self.node_class(text, **self.options)
        self.add_name(admonition_node)

        title_text = self.arguments[0]
        textnodes, messages = self.state.inline_text(title_text,
                                                     self.lineno)
        admonition_node += nodes.title(title_text, '', *textnodes)
        admonition_node += messages
        if not 'classes' in self.options:
            admonition_node['classes'] += ['admonition-' +
                                           nodes.make_id(title_text)]
        self.state.nested_parse(self.content, self.content_offset,
                                admonition_node)

        return [admonition_node]
