#!/usr/bin/env python
# encoding: utf-8
"""django-rewards is an affiliate marketing tool.
"""

# setup.py
# Created by Maximillian Dornseif on 2010-01-26 for HUDORA.
# Copyright (c) 2010 HUDORA. All rights reserved.

from setuptools import setup, find_packages

setup(name='django-rewards',
      maintainer='Maximillian Dornseif',
      # maintainer_email='xXXXx@hudora.de',
      version='1.0',
      description='xXXXx FILL IN HERE xXXXx',
      long_description=long_description=codecs.open('README.rst', "r", "utf-8").read(),
      classifiers=['License :: OSI Approved :: AGPL3 License',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python'],
      package_data={"django-rewards": ["templates/django-rewards/*.html", "reports/*.jrxml", "bin/*"]},
      packages=find_packages(),
      include_package_data=True,
      install_requires=['huTools', 'huDjango'],
      dependency_links = ['http://cybernetics.hudora.biz/dist/',
                          'http://cybernetics.hudora.biz/nonpublic/eggs/'],
)
