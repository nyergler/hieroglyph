import os.path
import re
from unittest import TestCase

from hieroglyph.tests.util import with_sphinx
from hieroglyph.tests import util


class PathFixingTests(TestCase):

    @with_sphinx(
        buildername='slides',
        srcdir=util.test_root.parent/'with-blockdiag',
    )
    def test_image_paths_exist(self, sphinx_app):

        sphinx_app.build()

        IMG_RE = re.compile(r'img.*src="(.*)"')

        img_paths = IMG_RE.findall(
            open(sphinx_app.builddir/'slides'/'index.html').read()
        )

        for img_src in img_paths:
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        sphinx_app.builddir/'slides',
                        img_src,
                    ),
                ),
                msg='Path %s does not exist.' % img_src,
            )

    @with_sphinx(
        buildername='slides',
        srcdir=util.test_root.parent/'with-blockdiag',
    )
    def test_image_paths_exist_subdirs(self, sphinx_app):

        sphinx_app.build()

        IMG_RE = re.compile(r'img.*src="(.*)"')

        img_paths = IMG_RE.findall(
            open(sphinx_app.builddir/'slides'/'subdir'/'index.html').read()
        )

        for img_src in img_paths:
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        sphinx_app.builddir/'slides'/'subdir',
                        img_src,
                    ),
                ),
                msg='Path %s does not exist.' % img_src,
            )
