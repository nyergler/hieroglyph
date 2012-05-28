import builder
import directives
import html


def setup(app):

    app.add_builder(builder.SlideBuilder)
    app.add_builder(builder.DirectorySlideBuilder)

    app.add_config_value('slide_theme', 'slides', 'html')
    app.add_config_value('slide_levels', 3, 'html')
    app.add_config_value('slide_theme_options', {}, 'html')
    app.add_config_value('slide_theme_path', [], 'html')

    # support for linking html output to slides
    app.add_config_value('slide_link_html_to_slides', False, 'html')
    app.add_config_value('slide_relative_path', '../slides/', 'html')


    app.add_node(directives.slides)
    app.add_directive('notslides', directives.Slides)
    app.add_directive('slides', directives.Slides)
    app.connect('doctree-resolved', directives.process_slide_nodes)

    app.connect('builder-inited', html.inspect_config)
    app.connect('html-page-context', html.add_link)
