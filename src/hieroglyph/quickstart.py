import datetime
import pkg_resources

from argparse import ArgumentParser
from sphinx.util.console import bold
import sphinx.quickstart

from hieroglyph import version


# redefine or extend some Sphixn declarations
sphinx.quickstart.MASTER_FILE = u"""
.. %(project)s slides file, created by
   hieroglyph-quickstart on %(now)s.


%(project)s
%(project_underline)s

Contents:

.. toctree::
   :maxdepth: %(mastertocmaxdepth)s

%(mastertoctree)s

"""

sphinx.quickstart.QUICKSTART_CONF += u"""

# -- Hieroglyph Slide Configuration ------------

extensions += [
    'hieroglyph',
]

slide_title = '%(project_str)s'
slide_theme = '%(slide_theme)s'
slide_levels = 3

# Place custom static assets in the %(dot)sstatic directory and uncomment
# the following lines to include them

# slide_theme_options = {
#     'custom_css': 'custom.css',
#     'custom_js': 'custom.js',
# }

# ----------------------------------------------

"""

sphinx.quickstart.MAKEFILE += u"""

slides:
	$(SPHINXBUILD) -b slides $(ALLSPHINXOPTS) $(BUILDDIR)/slides
	@echo "Build finished. The HTML slides are in $(BUILDDIR)/slides."

"""

batchfile = sphinx.quickstart.BATCHFILE
sphinx.quickstart.BATCHFILE = batchfile[:batchfile.rfind("\n:end\n")]
sphinx.quickstart.BATCHFILE += u"""
if "%%1" == "slides" (
\t%%SPHINXBUILD%% -b slides %%ALLSPHINXOPTS%% %%BUILDDIR%%/slides
\tif errorlevel 1 exit /b 1
\techo.
\techo.Build finished. The HTML slides pages are in %%BUILDDIR%%/slides.
\tgoto end
)

:end

"""

sphinx_ask_user = sphinx.quickstart.ask_user

def ask_user(d):
    """Wrap sphinx.quickstart.ask_user, and add additional questions."""

    # Print welcome message
    msg = bold('Welcome to the Hieroglyph %s quickstart utility.') % (
        version(),
    )
    print(msg)
    msg = """
This will ask questions for creating a Hieroglyph project, and then ask
some basic Sphinx questions.
"""
    print(msg)

    # set a few defaults that we don't usually care about for Hieroglyph
    d.update({
        'version': datetime.date.today().strftime('%Y.%m.%d'),
        'release': datetime.date.today().strftime('%Y.%m.%d'),
        'ext_autodoc': False,
        'ext_doctest': True,
        'ext_intersphinx': True,
        'ext_todo': True,
        'ext_coverage': True,
        'ext_pngmath': True,
        'ext_mathjax': False,
        'ext_ifconfig': True,
        'ext_viewcode': False,
    })

    if 'project' not in d:
        print('''
The presentation title will be included on the title slide.''')
        sphinx.quickstart.do_prompt(d, 'project', 'Presentation title')
    if 'author' not in d:
        sphinx.quickstart.do_prompt(d, 'author', 'Author name(s)')

    # slide_theme
    theme_entrypoints = pkg_resources.iter_entry_points('hieroglyph.theme')

    themes = [
        t.load()
        for t in theme_entrypoints
    ]

    msg = """
Available themes:

"""

    for theme in themes:
        msg += '\n'.join([
            bold(theme['name']),
            theme['desc'],
            '', '',
        ])

    msg += """Which theme would you like to use?"""
    print(msg)

    sphinx.quickstart.do_prompt(
        d, 'slide_theme', 'Slide Theme', themes[0]['name'],
        sphinx.quickstart.choice(
            *[t['name'] for t in themes]
        ),
    )

    # Ask original questions
    print("")
    sphinx_ask_user(d)


def quickstart(path=None):

    d = {}
    if path:
        d['path'] = path

    ask_user(d)
    sphinx.quickstart.generate(d)


def main():
    parser = ArgumentParser(
        description='Run hieroglyph -q to start a presentation',
    )

    parser.add_argument('-v', '--version', action='store_true',
                        help="Print current version of hieroglyph")
    parser.add_argument('-q', '--quickstart', action='store_true',
                        help="Start a hieroglyph project")

    parser.add_argument('path', nargs='?', default=None,
                        help='Output directory for new presentation.')

    args = vars(parser.parse_args())

    if (args['version']):
        print(version())
    elif (args['quickstart']):
        quickstart(args['path'])
