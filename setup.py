# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in doppelpass/__init__.py
from doppelpass import __version__ as version

setup(
	name='doppelpass',
	version=version,
	description='Doppelpass Beschreibung',
	author='msmr.ch',
	author_email='info@msmr.ch',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
