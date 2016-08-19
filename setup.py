from setuptools import setup, find_packages
import os

version = '1.1'

setup(name='eea.zopefindsupportpatch',
      version=version,
      description=("A patch for the OFS.FindSupport module"),
      long_description=open("README.txt").read() + "\n" +
      open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=["Programming Language :: Python",
                   ],
      keywords='',
      author='Valentin Dumitru',
      author_email='valentin.dumitru@gmail.com',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'importlib',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
