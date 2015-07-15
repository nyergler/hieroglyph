"""Writer Support for Hieroglyph Slides."""

from docutils import nodes
from docutils.writers.html4css1 import HTMLTranslator as BaseTranslator
from sphinx.writers.html import HTMLTranslator
from hieroglyph import html
from hieroglyph.directives import slideconf


class SlideData(object):

    def __init__(self, translator, **kwargs):

        # set during init, see below (there only 1 call!)
        self._translator = translator
        self.id = ''
        self.level = 0
        self.slide_number = 0
        self.classes = []

        # set after init (direct write)
        self.title = None
        self.content = ''

        # no other attrs are used then above!
        for name, value in kwargs.items():  setattr(self, name, value)


    def _filter_classes(self, include=None, exclude=None):
        classes = self.classes[:]
        if include is not None:
            classes = [ c[len(include):] for c in classes if c.startswith(include) ]
        if exclude is not None:
            classes = [ c for c in classes if not c.startswith(exclude) ]
        return classes


    def _get_slide_context(self):
        """Return the context dict for rendering this slide."""

        return { 'title': "" if self.title is None else self.title,
                 'level': self.level,
                 'content': self.content,
                 'classes': self.classes,
                 'slide_classes': self._filter_classes(exclude='content-'),
                 'content_classes': self._filter_classes(include='content-'),
                 'slide_number': self.slide_number,
                 'config': self._translator.builder.config,
                 'id': self.id }


class BaseSlideTranslator(HTMLTranslator):

    def __init__(self, *args, **kwargs):

        HTMLTranslator.__init__(self, *args, **kwargs)

        self.slide_number = 0
        self.body_stack = []
        self.current_slide = None
        #self.slide_data = []


    def push_body(self):
        """Push the current body onto the stack and create an empty one."""

        self.body_stack.append(self.body)
        self.body = []

    def pop_body(self):
        """Replace the current body with the last one pushed to the stack."""
        self.body = self.body_stack.pop()


    def visit_slideconf(self, node):
        pass

    def depart_slideconf(self, node):
        pass


    def slide_start(self, node): #GAM: renamed
        """A pseudo visitor for slides; as `slides` isn't a docutils node, it can't be visited. It
           is called in the writer to start a (new) slide. Typically on a new section."""
        # NOTE: for this to work 100%, the slide directive has to be changed to work to
        #       That directive is not creating a slide tag ... (no really valid)
        #       Make it work like the nextslide directive, that one is OL

        self.slide_number +=1

        classes = node.get('classes')
        if not classes:
            slide_conf = slideconf.get_conf(self.builder, node.document)
            classes = slide_conf['slide_classes']

        self.current_slide = SlideData(translator=self, id=node.get('ids', ("",))[0],  # first ID of empty string
                                       level=self.section_level, slide_number=self.slide_number,
                                       classes=classes)
        self.push_body() # collect `body` data inside the slide, to render and append it during slide_end

    def slide_end(self, node): #GAM: renamed
        ## """Also see `slide_start; this is the matching` pseudo depart for slides. Always called by a writer"""

        # All `body` of the slide is collected; get it and pop the body
        slide_body= self.body
        self.pop_body()

        slide = self.current_slide
        slide.content = u''.join(slide_body)

        rendered_slide = self.builder.templates.render('slide.html', slide._get_slide_context())
        self.body.append(rendered_slide)
        self.current_slide = None


    def visit_title(self, node):
        if (self.current_slide is not None) and (self.current_slide.title is None):
            # This is the first title in on a new slide -> Put in current_slide title. Not in the body/content
            self.current_slide.title = node.astext().strip()
            raise nodes.SkipNode   # will skip depart_title!
        else:
            HTMLTranslator.visit_title(self, node)

    ## # Not really needed, as only the inherited method is used
    ## def depart_title(self, node): # Not called when title of current_slide is set!
    ##     HTMLTranslator.depart_title(self, node)

    def visit_block_quote(self, node):
        quote_slide_tags = ['paragraph', 'attribution']

        # see if this looks like a quote slide
        if (len(node.children) <= 2 and
            [c.tagname for c in node.children] == quote_slide_tags[:len(node.children)]):

            # process this as a quote slide

            # first child must be a paragraph, process it as a <q> element
            p = node.children[0]
            self.body.append(self.starttag(node, 'q'))
            for text_item in p:
                text_item.walkabout(self)
                self.body.append('</q>\n')

            # optional second child must be an attribution, processing as a <div>
            # following the <q>
            if len(node.children) > 1:
                attr = node.children[1]

                self.body.append(self.starttag(attr, 'div', CLASS="author"))
                for text_item in attr:
                    text_item.walkabout(self)
                    self.body.append('</div>\n')

            # skip all normal processing
            raise nodes.SkipNode

        else:
            return HTMLTranslator.visit_block_quote(self, node)


class SlideTranslator(BaseSlideTranslator):

    def visit_section(self, node):
        #  Increase the section_level, and  'maybe' start a new slide
        self.section_level += 1
        self._maybe_new_slide(node)         # we might need a new slide (stop one and start one)

    def depart_section(self, node):
        self.section_level -= 1


    def _maybe_new_slide(self, node):
        """Determine whether a slide-transition is needed, and insert it when needed.
           Also return True/False depending on that need."""

        if not slideconf.get_conf(self.builder, node.document)['autoslides']:
            return False
        # else

        slide_levels = self.builder.config.slide_levels

        if self.section_level <= slide_levels:
            if getattr(self, 'slide_open', False): #  Basically: Skip slide_end, for when starting the first slide!
                self.slide_end(node)

            self.slide_start(node)
            self.slide_open=True

            return True
        else:
            return False


    def visit_document(self, node): # Only to TRACE it
        BaseSlideTranslator.visit_document(self, node)


    def depart_document(self, node):
        if getattr(self, 'slide_open', False):         #Close the last slide
            self.slide_end(node)
        BaseSlideTranslator.depart_document(self, node)


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

        BaseSlideTranslator.depart_title(self, node)

    def visit_start_of_file(self, node):
        previous = node.parent
        if isinstance(previous, nodes.compound):
            # step up one more level
            previous = previous.parent

        self.depart_slide(previous)
        self.section_level -= 1

        BaseSlideTranslator.visit_start_of_file(self, node)



class SingleFileSlideTranslator(SlideTranslator):

    def visit_compound(self, node):
        if not 'toctree-wrapper' in node['classes']:
            SlideTranslator.visit_compound(self, node)

    def depart_compound(self, node):
        if not 'toctree-wrapper' in node['classes']:
            SlideTranslator.depart_compound(self, node)
