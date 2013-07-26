import datetime

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
    print bold('Welcome to the Hieroglyph %s quickstart utility.') % (
        version(),
    )
    print """
This will ask questions for creating a Hieroglyph project, and then ask
some basic Sphinx questions.
"""

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
        print '''
The presentation title will be included on the title slide.'''
        sphinx_quickstart.do_prompt(d, 'project', 'Presentation title')
    if 'author' not in d:
        sphinx_quickstart.do_prompt(d, 'author', 'Author name(s)')

    # slide_theme
    print """
Hieroglyph includes two themes:

* """ + bold("slides") + """
  The default theme, with different styling for first, second, and third
  level headings.

* """ + bold("single-level") + """
  All slides are styled the same, with the heading at the top.

Which theme would you like to use?"""

    # XXX make a themes dict that has the keys/descriptions
    sphinx_quickstart.do_prompt(
        d, 'slide_theme', 'Slide Theme', 'slides',
        sphinx_quickstart.choice('slides', 'single-level',),
    )

    # Ask original questions
    print
    sphinx_ask_user(d)


sphinx_quickstart.ask_user = ask_user

def main():
    sphinx_quickstart.main()
