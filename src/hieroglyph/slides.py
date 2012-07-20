from hieroglyph.builder import building_slides

EXTRA_PAGES = ('console',)


def __fix_context(context):
    """Return a new context dict based on original context.

    The new context will be a copy of the original, and some mutable
    members (such as script and css files) will also be copied to
    prevent polluting shared context.
    """

    COPY_LISTS = ('script_files', 'css_files',)

    for attr in COPY_LISTS:
        if attr in context:
            context[attr] = context[attr][:]

    return context


def slide_context(app, pagename, templatename, context, doctree):
    """Update the context when building Slides."""

    if building_slides(app):

        # make a copy so we don't pollute the shared context
        context = __fix_context(context)

        if pagename not in EXTRA_PAGES:

            context['script_files'].append('_static/common.js')
            context['script_files'].append('_static/slides.js')
            context['script_files'].append('_static/sync.js')
            context['script_files'].append('_static/controller.js')
            context['script_files'].append('_static/init.js')

    return context

def get_pages(app):

    if building_slides(app):

        # include the slide console
        context = __fix_context(app.builder.globalcontext.copy())
        context['css_files'].append('_static/console.css')
        context['script_files'].append('_static/common.js')
        context['script_files'].append('_static/console.js')
        context['title'] = 'Presenter Console'

        return [
            ('console', context, 'console.html',),
        ]

    return []
