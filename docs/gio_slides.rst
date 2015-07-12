================
Google IO slides
================

The theme ``slides2`` enables a modern slidedeck, based on the one Google introduced for I/O 2012;
and still updates. It has support for mobile/touch devices too. But it not fully compatible with
the (original) `slides` and `single-level` themas.

Currently the options are partly described in the :ref:`original documentation
<org_doc_gio_slides>` and partly here. This page is work in progress (as is the code support).

Presenting
**********

For *presenter-mode*, **start** the page with the suffix `?presentme=true`; use an URL without
page-suffix (#<no>). The keyboard option 'c' does not (yet) work.  In this mode, two windows are
shown, typically on 2 (physical) screens: a normal one for the audience, and one with more info for
the presenter.

Note: presenter-mode and presentation-links don't work correctly. Links are (only) clickable in the
'audience' window; they open the presentation in a new tab/window, bu no presenter-window will
pop-up!

Keyboard control
=================

.. note:: The action-keys are hardcodes in ``js/slide-deck.js``
   (function: :js:func:`SlideDeck.prototype.onBodyKeyDown_` )

Navigation
----------

============	===================================	===============
*Action*	*Keys*					*Remarks*
------------	-----------------------------------	---------------
**Next**	RightArrow, Space, PgDn, DownArrow	GoTo next slide
**Back**	LeftArrow, Backspace, PgUp, UpArrow
============	===================================	===============



Toggles
-------

============	========================	========================================================
*Key*		*Action*			*Remarks*
------------	------------------------	--------------------------------------------------------
**w**		wide/narrow-screen		change width of the slide, dynamically
**o**		overview mode			Show all slides as miniatures
*<Enter>*	overview mode			Displays the 'overview'-class, when available
**p**		show speaker notes		if they're on the current slide
**f**		fullscreen viewing		when browser supports it; not on Safari)
**h**		code highlighting		XXX
============	========================	========================================================

Keys are not case-sensitive. Most options can be toggled 'off' with **ESC** (has no effect on wide/narrow).

NOTES
*****

* Each slidedeck (file) will automatically become a title- and end-slide. Both will have an icon,
  that should be named ``title_icon.png`` and ``end_icon.png`` and should be places in the
  ``_static/slides2/`` directory. Those images will be (css) scaled, to 128*128 pixels (by default;
  this can be changed in CSS XXX).
* Do **NOT** add a newline (`\n`) in the title (version/releases string). It will break the slides;
  and shows *noting*
