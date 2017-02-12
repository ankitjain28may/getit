#!/usr/bin/env python

from setuptools import setup
import sys  # noqa

setup(
    name='getit',
    version='2.0',
    description='A cross platform CLI downloader tool written in python.',
    long_description=open('README.rst').read(),
    author='Ankit Jain',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords="download cli, downloaded-tool, cross-platform-cli-downloader",
    author_email='ankitjain28may77@gmail.com',
    url='https://github.com/ankitjain28may/getit',
    packages=['getit'],
    install_requires=[
        'configparser>=3.5.0',
        'requests==2.10.0',
        'colorama>=0.3.7'
    ],
    entry_points={
        'console_scripts': [
            'getit = getit.getit:main'
            ],
    }
)
