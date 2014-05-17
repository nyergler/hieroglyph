import datetime

from argparse import ArgumentParser
from sphinx.util.console import bold
from sphinx import quickstart as sphinx_quickstart

from hieroglyph import version


# redefine or extend some Sphixn declarations
sphinx_quickstart.MASTER_FILE = u"""
.. %(project)s slides file, created by
   hieroglyph-quickstart on %(now)s.


%(project)s
%(project_underline)s

Contents:

.. toctree::
   :maxdepth: %(mastertocmaxdepth)s

%(mastertoctree)s

"""

sphinx_quickstart.QUICKSTART_CONF += u"""

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

sphinx_quickstart.MAKEFILE += u"""

slides:
    $(SPHINXBUILD) -b slides $(ALLSPHINXOPTS) $(BUILDDIR)/slides
    @echo "Build finished. The HTML slides are in $(BUILDDIR)/slides."

"""

sphinx_quickstart.BATCHFILE += u"""

if "%%1" == "slides" (
\t%%SPHINXBUILD%% -b slides %%ALLSPHINXOPTS%% %%BUILDDIR%%/slides
\tif errorlevel 1 exit /b 1
\techo.
\techo.Build finished. The HTML slides pages are in %%BUILDDIR%%/slides.
\tgoto end
)

"""

sphinx_ask_user = sphinx_quickstart.ask_user

def ask_user(d):
    """Wrap sphinx_quickstart.ask_user, and add additional questions."""

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
        sphinx_quickstart.do_prompt(d, 'project', 'Presentation title')
    if 'author' not in d:
        sphinx_quickstart.do_prompt(d, 'author', 'Author name(s)')

    # slide_theme
    msg = """
Hieroglyph includes two themes:

* """ + bold("slides") + """
  The default theme, with different styling for first, second, and third
  level headings.

* """ + bold("single-level") + """
  All slides are styled the same, with the heading at the top.

Which theme would you like to use?"""
    print(msg)

    # XXX make a themes dict that has the keys/descriptions
    sphinx_quickstart.do_prompt(
            d, 'slide_theme', 'Slide Theme', 'single-level',
            sphinx_quickstart.choice('slides', 'single-level',),
            )

    # Ask original questions
    print("")
    sphinx_ask_user(d)


sphinx_quickstart.ask_user = ask_user

def compatibility():
    sphinx_quickstart.main()

def main():
    parser = ArgumentParser()
    parser.add_argument('hieroglyph', nargs='?', help="Run hieroglyph -q to start a presentation")
    parser.add_argument('-v', '--version', action='store_true', help="Print current version of hieroglyph")
    parser.add_argument('-q', '--quickstart', action='store_true', help="Start a hieroglyph project")
    args = vars(parser.parse_args())
    if (args['version']):
        print(version())
    elif (args['quickstart']):
        sphinx_quickstart.main()
