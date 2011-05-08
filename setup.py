from setuptools import setup, find_packages
import os, sys

execfile('exemelopy/__version__.py')

setup(name="exemelopy",
      description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
      version=__version__,
      url="http://unpluggd/exemelopy",
      packages=find_packages(exclude=["specs","benchmark"]),
      install_requires=['lxml','ordereddict'],
      )
      
