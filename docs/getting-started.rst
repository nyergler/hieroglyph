=================================
 Getting Started with Hieroglpyh
=================================

Hieroglyph is an extension for `Sphinx`_ which builds HTML slides from
`ReStructured Text`_ documents. Hieroglyph lets you leverage Sphinx
and its large collection of extensions to create rich documents that
are accessible to anyone with a web browser. It also includes tools
that help you, as the presenter, to share your presentation.

This document walks through creating a presentation with Hieroglyph
and Sphinx. After reading this, you will be able to use Hieroglyph to
create slides, and be ready to explore additional features and
extensions available through Sphinx.

.. _Sphinx: http://sphinx.pocoo.org/
.. _docutils: http://docutils.sourceforge.net/
.. _rst2s5: http://docutils.sourceforge.net/docs/user/slide-shows.html
.. _ifconfig: http://sphinx.pocoo.org/ext/ifconfig.html
.. _`HTML 5 Slides`: http://code.google.com/p/html5slides/
.. _`ReStructured Text`: http://docutils.sourceforge.net/

Install Hieroglyph and Dependencies
===================================

To get started, you need to install Hieroglyph and its dependencies.
Hieroglyph is written in Python_, so if you don't have that installed,
you'll need to install it first.

Once Python is installed, you can install Hieroglyph (along with an
dependencies it needs with `easy_install`_ or pip_.

::

  $ easy_install hieroglyph

Installing Hieroglyph will also install its dependencies, including
Sphinx_ and docutils_, if needed.

.. _Python: http://python.org
.. _`easy_install`: http://pythonhosted.org/distribute/easy_install.html
.. _pip: http://pip-installer.org

Create a Project
================

After you've installed Hieroglyph and Sphinx, you can create a new
project. A Sphinx project defines where to look for the source files
and what extensions to enable. You can start your project using the
:program:`sphinx-quickstart` program included with Sphinx.

::

  $ sphinx-quickstart

:program:`sphinx-quickstart` will ask you questions about your
project. Not all of these make sense if you're just creating a
presentation (as opposed to a presentation and other documentation
simultaneously), so you can usually just accept the defaults. You will
have to specify a project name and version.

:program:`sphinx-quickstart` will create several files, including
``conf.py``. ``conf.py`` contains the configuration for your project,
and you'll need to enable Hieroglyph before going further.

Open ``conf.py`` and find the ``extensions`` definition::

  extensions = []

Your definition may have items in the list if you answered "yes" to
any of the Sphinx Quickstart questions. We need to add ``hieroglyph``
to this list::

  extensions = ['hieroglyph']

That enables Hieroglyph for the project.


Authoring Slides
================

Once you've enabled Hieroglyph for your Sphinx project, you can begin
authoring your slides. Hieroglyph uses `ReStructured Text`_ for
slides, and by default sections in the document map to slides.

You can open up ``index.rst`` (assuming you chose the default name
when you ran quickstart) and add some content.

::

  ====================
   Presentation Title
  ====================

  First Slide
  ===========

  Some content on the first slide.

  Second Slide
  ============

  * A
  * Bulleted
  * List

Here we've made three slides: a title slide (with "Presentation Title"
on it), a first slide with a sentence on it, and a second slide with a
bulleted list.

Generating Your Slides
----------------------

Now that we've written some simple slides in ReStructured Text, we can
generate the HTML slides from that. To do that we use of the included
:ref:`builders`.

::

  $ sphinx-build -b slides . ./_build/slides

:program:`sphinx-build` will read the ``conf.py`` file, load the
``index.rst`` we've been editing, and generate the slides in the
``./_build/slides`` directory. After running :program:`sphinx-build`,
that directory will contain an ``index.html`` file, along with all of
the CSS and Javascript needed to render the slides.

Incremental slides
------------------

It's common to have a slide with a list of items that are shown one at
a time. Hieroglpyh supports this through the use of the ``build``
class. Let's add a third slide to ``index.rst`` that incrementally
displays a bulleted list.

::

  Show Bullets Incrementally
  ==========================

  .. rst-class:: build

  - Adding the ``build`` class to a container
  - To incrementally show its contents
  - Remember that *Sphinx* maps the basic ``class`` directive to
    ``rst-class``

Here the :rst:dir:`rst-class` directive causes the next element
to be built incrementally.

Displaying Images
-----------------

You can include any image in a slide using the :rst:dir:`image`
directive. Just drop them in the ``_static`` directory in your
project.

Hieroglyph also includes some support for showing an image as the full
slide using the :rst:dir:`figure` directive. For example, the
Hieroglyph introductory slide deck uses the following markup::

  .. figure:: /_static/hieroglyphs.jpg
     :class: fill

     CC BY-SA http://www.flickr.com/photos/tamburix/2900909093/

The caption (license information above) is styled as an overlay on the
image.

The ``slide`` directive
-----------------------

In addition to mapping ReStructured Text sections to slides, you can
create a slide at any point in your document using the
:rst:dir:`slide` directive. The :rst:dir:`slide` directive allows you
insert a slide at some place other than a heading. This can be useful
when you're writing a single document that you'll present as slides as
well as text. For example, if you're writing a narrative tutorial and
want to include the slides in the same document, the :rst:dir:`slide`
directive makes this straight-forward.

Let's consider how the example of an incremental slide would look
using the :rst:dir:`slide` directive::

  .. slide:: Show Bullets Incrementally
     :level: 2

     .. rst-class:: build

     - Adding the ``build`` class to a container
     - To incrementally show its contents
     - Remember that *Sphinx* maps the basic ``class`` directive to
       ``rst-class``

Note that here we need to specify the ``level`` option to let Sphinx
know which level this slide corresponds to. In Sphinx and Hieroglyph,
the document title is level 1, the next heading level is level 2, etc.

Unlike slides generated automatically from headings and content,
slides defined using the :rst:dir:`slide` directive will only show up
when generating slides. If you generate normal HTML output or a PDF of
your Sphinx project, the contents of the directive will be removed.

This example shows how to add slides with the :rst:dir:`slide`
directive, but sometimes you *only* want to use :rst:dir:`slide`
directives. In that case you can disable :confval:`autoslides`.

Slide-only and non-slide content
--------------------------------

Another useful tool for mixing narrative documentation with slides is
the ability to exclude content from slides or vice versa. Hieroglyph
provides two directives for just this purpose. The :rst:dir:`ifslides`
directive only includes its contents when building slides. The
counterpart, :rst:dir:`ifnotslides`, only includes its content when
building other targets. The latter, in particular, may be used to
include notes that you'd like to print with HTML or PDF output, but
not include in the slides.

Viewing Your Slides
===================

When you open the slide HTML in your browser, it looks something like
this:

.. image:: /_static/slide_show.png

You can use the space bar to advance to the next slide, or the left
and right arrows to move back and forward, respectively.

Sometimes you want to skim through your slides quickly to find
something, or jump ahead or back. You can use the *Slide Table* view
for this. Just press ``t`` in the browser and the slides will shrink
down.

.. image:: /_static/slide_table.png

You can click on a slide to jump there, or press ``t`` again to exit
the slide table.

Presenter Console
-----------------

If you're presenting your slides, it's often helpful to be able to see
what's coming next. Hieroglyph includes a *Presenter's Console* for
this purpose. Just press ``c`` when viewing the slides and the console
will open in a new window.

.. image:: /_static/slide_console.png

Moving the slides backward or forward in either window will keep the
other in sync.

Styling Your Slides
===================

The simplest way to style your presentation is to add a custom CSS
file. There are two steps to adding custom CSS: first, create the CSS
file, and second, tell Hieroglyph to include it in the output.

Hieroglyph generates ``article`` tags for slides, and adds classes
based on their level. That's enough to start some basic styling.
Create a new file, ``custom.css``, in the ``_static`` directory in
your project. For this example, we'll change the background color of
all slides to light blue, and make the title slide's text (``<h1>``)
red.

.. code-block:: css

   article {
       background-color: light-blue;
   }

   article h1 {
       color: red;
   }


The ``_static`` directory contains static assets that can be included
in your output.

After you've created your CSS file, tell Sphinx about it by setting
:confval:`slide_theme_options` in ``conf.py``::

  slide_theme_options = {'custom_css': 'custom.css'}

After you re-build your slides, you'll see the new CSS take effect.

Additional Options
==================

Hieroglyph has several configuration options which allow you to
control how it generates slides and how those slides are connected to
HTML output. See :reF:`hieroglyph-configuration` for a full list.

Sphinx Extensions
=================

Hieroglyph is built on Sphinx, which has a wide variety of extensions
available. These extensions can help you `create diagrams`_, `include
code`_ snippets, `render mathematical formulas`_, or `embed maps`_.
All of these extensions are available to Hieroglpyh, which makes it a
flexible and extensible program for creating presentations.


.. _`create diagrams`: https://pypi.python.org/pypi/sphinxcontrib-blockdiag/
.. _`include code`: https://pypi.python.org/pypi/tut/
.. _`render mathematical formulas`: http://sphinx-doc.org/ext/math.html
.. _`embed maps`: https://pypi.python.org/pypi/sphinxcontrib-googlemaps/
