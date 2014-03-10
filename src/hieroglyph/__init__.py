import unicodedata

from hieroglyph import builder
from hieroglyph import directives
from hieroglyph import html
from hieroglyph import slides


def version():
    """Return the installed package version."""

    import pkg_resources

    return pkg_resources.get_distribution('hieroglyph').version


def setup(app):

    # Register Builders
    app.add_builder(builder.SlideBuilder)
    app.add_builder(builder.DirectorySlideBuilder)
    app.add_builder(builder.InlineSlideBuilder)
    app.add_builder(builder.DirectoryInlineSlideBuilder)

    app.connect('html-collect-pages', slides.get_extra_pages)

    # core slide configuration
    app.add_config_value('slide_title', None, 'html')
    app.add_config_value('slide_theme', 'slides', 'html')
    app.add_config_value('slide_levels', 3, 'html')
    app.add_config_value('slide_theme_options', {}, 'html')
    app.add_config_value('slide_theme_path', [], 'html')
    app.add_config_value('slide_numbers', False, 'html')
    app.add_config_value('slide_footer', None, 'html')
    app.add_config_value('autoslides', True, 'env')

    # support for linking html output to slides
    app.add_config_value('slide_link_html_to_slides', False, 'html')
    app.add_config_value('slide_link_html_sections_to_slides', False, 'html')
    app.add_config_value('slide_relative_path', '../slides/', 'html')
    app.add_config_value('slide_html_slide_link_symbol',
                         unicodedata.lookup('section sign'), 'html')

    # support for linking from slide output to html
    app.add_config_value('slide_link_to_html', False, 'html')
    app.add_config_value('slide_html_relative_path', '../html/', 'html')

    # slide-related directives
    app.add_node(directives.if_slides)
    app.add_directive('ifnotslides', directives.IfBuildingSlides)
    app.add_directive('ifslides', directives.IfBuildingSlides)
    app.add_directive('notslides', directives.IfBuildingSlides)
    app.add_directive('slides', directives.IfBuildingSlides)
    app.add_transform(directives.TransformSlideConditions)

    app.add_node(directives.slideconf,
                 html=(directives.raiseSkip, None),
                 latex=(directives.raiseSkip, None),
                 text=(directives.raiseSkip, None),
                 man=(directives.raiseSkip, None),
                 texinfo=(directives.raiseSkip, None),
    )
    app.add_directive('slideconf', directives.SlideConf)
    app.connect('doctree-resolved', directives.process_slideconf_nodes)

    app.add_node(directives.slide)
    app.add_directive('slide', directives.SlideDirective)
    app.connect('doctree-resolved', directives.process_slide_nodes)

    app.add_node(directives.nextslide)
    app.add_directive('nextslide', directives.NextSlideDirective)
    app.add_transform(directives.TransformNextSlides)

    app.connect('builder-inited', html.inspect_config)
    app.connect('html-page-context', html.add_link)
