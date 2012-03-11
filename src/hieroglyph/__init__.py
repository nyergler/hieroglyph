import builder

def setup(app):

    app.add_builder(builder.SlideBuilder)
    app.add_builder(builder.DirectorySlideBuilder)

    app.add_config_value('slide_theme', 'slides', 'html')
    app.add_config_value('slide_levels', 3, 'html')
    app.add_config_value('slide_theme_options', {}, 'html')
    app.add_config_value('slide_theme_path', [], 'html')
