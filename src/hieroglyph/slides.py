from hieroglyph.builder import building_slides


def slide_context(app, pagename, templatename, context, doctree):
    """Update the context when building Slides."""

    if building_slides(app):

        # make a copy so we don't pollute the shared context
        context['script_files'] = context['script_files'][:]

        # add the slides javascript
        context['script_files'].append('_static/common.js')
        context['script_files'].append('_static/slides.js')

        # add additional code for additional pages
        if pagename == 'console':
            context['script_files'].append('_static/console.js')

    return context
