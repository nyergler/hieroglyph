from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.7.1'

install_requires = [
    "setuptools",
    "Sphinx >= 1.2",
    "six",
]


setup(name='hieroglyph',
      version=version,
      description=("Generate HTML presentations from plain text "
                   "sources with all the power of Sphinx."),
      long_description=README + '\n\n' + NEWS,
      classifiers=[
        'License :: OSI Approved :: BSD License',
        'Topic :: Documentation',
        'Topic :: Text Processing',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
      ],
      keywords='',
      author='Nathan Yergler',
      author_email='nathan@yergler.net',
      url='https://github.com/nyergler/hieroglyph',
      license='BSD',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points={
          'console_scripts': [
              'hieroglyph=hieroglyph.quickstart:main',
              'hieroglyph-quickstart=hieroglyph.quickstart:quickstart',
          ],
          'hieroglyph.theme': [
              'slides=hieroglyph.themes:SLIDES',
              'single-level=hieroglyph.themes:SINGLE_LEVEL',
              'slides2=hieroglyph.themes:SLIDES2',
          ],
      },
      test_suite='hieroglyph.tests',
      tests_require=[
          'beautifulsoup4',
          'mock',
          'sphinx-testing',
      ],
      )
