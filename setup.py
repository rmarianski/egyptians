from setuptools import setup, find_packages
import sys, os

version = '0.0'

requires = [
    'ZODB3',
    'pyramid',
    'repoze.folder',
    ]

setup(name='egyptians',
      version=version,
      description="user functionality for pyramid in a zodb context",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Robert Marianski',
      author_email='rob@marianski.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite='egyptians',
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
