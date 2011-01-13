from setuptools import setup, find_packages
import os, sys

execfile('exemelopy/__version__.py')

setup(name="FWRD",
      description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
      version=__version__,
      url="http://digitala.github.com/exemelopy",
      packages=find_packages(exclude="specs"),
      install_requires=['lxml','ordereddict'],
      )
      
