#!/usr/env python
""" InstaBus is a crowdsourcing application for the improvement 
of public transportation in Bucharest, Romania.
"""

from setuptools import setup, find_packages

setup(
    name='InstaBus',
    version='0.0.1-dev',
    url='https://github.com/alexbardas/instabus',
    license='MIT',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    test_suite=''
)
