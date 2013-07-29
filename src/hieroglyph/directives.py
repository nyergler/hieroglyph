from docutils import nodes

from sphinx.util.nodes import set_source_info
from docutils.nodes import SkipNode
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives import (
    admonitions,
)
from docutils.parsers.rst.roles import set_classes


def raiseSkip(self, node):
    raise SkipNode()


class if_slides(nodes.Element):
    pass


class IfBuildingSlides(Directive):

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}

    def run(self):
        if self.name in ('slides', 'notslides',):
            import warnings

            # these are deprecated, print a warning
            warnings.warn(
                "The %s directive has been deprecated; replace with if%s" % (
                    self.name, self.name,
                ),
                stacklevel=2,
            )

        node = if_slides()
        node.document = self.state.document
        set_source_info(self, node)

        node.attributes['ifslides'] = self.name in ('slides', 'ifslides',)

        self.state.nested_parse(self.content, self.content_offset,
                                node, match_titles=1)
        return [node]


def process_slidecond_nodes(app, doctree, docname):

    from hieroglyph import builder

    is_slides = builder.building_slides(app)

    # this is a slide builder, remove notslides nodes
    for node in doctree.traverse(if_slides):

        keep_content = is_slides == node.attributes.get('ifslides', False)

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

        if 'theme' in self.attributes:
            builder.pop_theme()

    @classmethod
    def get(cls, doctree):
        """Return the first slideconf node for the doctree."""

        conf_nodes = doctree.traverse(cls)
        if conf_nodes:
            return conf_nodes[0]

    @classmethod
    def get_conf(cls, builder, doctree=None):
        """Return a dictionary of slide configuration for this doctree."""

        # set up the default conf
        result = {
            'theme': builder.config.slide_theme,
            'autoslides': builder.config.autoslides,
            'slide_classes': [],
        }

        # now look for a slideconf node in the doctree and update the conf
        if doctree:
            conf_node = cls.get(doctree)
            if conf_node:
                result.update(conf_node.attributes)

        return result


def boolean_option(argument):

    return str(argument.strip().lower()) in ('true', 'yes', '1')


class SlideConf(Directive):

    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'theme': directives.unchanged,
        'autoslides': boolean_option,
        'slide_classes': directives.class_option,
    }

    def run(self):
        node = slideconf(**self.options)
        node.document = self.state.document
        set_source_info(self, node)

        return [node]


def no_autoslides_filter(node):

    if isinstance(node, (if_slides, slideconf, slide)):
        return True

    if (isinstance(node, nodes.section) and
            'include-as-slide' in node.attributes.get('classes', [])):
        node.attributes['include-as-slide'] = True

        remove_classes = ['include-as-slide']
        # see if there's a slide-level class, too
        for cls_name in node.attributes['classes']:
            if cls_name.startswith('slide-level-'):
                node.attributes['level'] = int(cls_name.rsplit('-', 1)[-1])
                remove_classes.append(cls_name)

        ## for cls_name in remove_classes:
        ##     node.attributes['classes'].remove(cls_name)

        return True

    return False


def filter_doctree_for_slides(doctree):
    """Given a doctree, remove all non-slide related elements from it."""

    current = 0
    num_children = len(doctree.children)
    while current < num_children:

        child = doctree.children[current]
        child.replace_self(
            child.traverse(no_autoslides_filter)
        )

        if len(doctree.children) == num_children:
            # nothing removed, increment current
            current += 1
        else:
            # a node was removed; retain current and update length
            num_children = len(doctree.children)


def process_slideconf_nodes(app, doctree, docname):

    from hieroglyph import builder

    is_slides = builder.building_slides(app)

    # if autoslides is disabled and we're building slides,
    # replace the document tree with only explicit slide nodes
    if (is_slides and
            not slideconf.get_conf(app.builder, doctree)['autoslides']):

        filter_doctree_for_slides(doctree)


class slide(nodes.admonition):
    pass


class SlideDirective(admonitions.Admonition):

    required_arguments = 0
    optional_arguments = 1
    node_class = slide
    option_spec = {
        'class': directives.class_option,
        'name': directives.unchanged,
        'level': directives.nonnegative_int,
        'inline-contents': boolean_option,
    }

    def run(self):

        # largely lifted from the superclass in order to make titles work
        set_classes(self.options)
        # self.assert_has_content()
        text = '\n'.join(self.content)
        admonition_node = self.node_class(text, **self.options)
        self.add_name(admonition_node)

        if self.arguments:
            title_text = self.arguments[0]
            textnodes, messages = self.state.inline_text(title_text,
                                                         self.lineno)
            admonition_node += nodes.title(title_text, '', *textnodes)
            admonition_node += messages
        else:
            # no title, make something up so we have an ID
            title_text = str(hash(' '.join(self.content)))

        if not 'classes' in self.options:
            admonition_node['classes'] += ['admonition-' +
                                           nodes.make_id(title_text)]
        self.state.nested_parse(self.content, self.content_offset,
                                admonition_node)

        return [admonition_node]


def process_slide_nodes(app, doctree, docname):

    from hieroglyph import builder

    supports_slide_nodes = (
        builder.building_slides(app) or
        isinstance(app.builder, builder.AbstractInlineSlideBuilder)
    )

    if supports_slide_nodes:
        return

    # this builder does not understand slide nodes; remove them
    for node in doctree.traverse(slide):
        if node.attributes.get('inline-contents', False):
            node.replace_self(node.children[1:])
        else:
            node.replace_self(nodes.inline())
