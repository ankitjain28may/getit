# getit

[![Build Status](https://travis-ci.org/ankitjain28may/getit.svg?branch=master)](https://travis-ci.org/ankitjain28may/getit)
[![PyPI](https://img.shields.io/pypi/v/getit.svg)](https://pypi.python.org/pypi/getit)
[![PyPI](https://img.shields.io/pypi/dm/getit.svg)](https://pypi.python.org/pypi/getit)
[![Code Health](https://landscape.io/github/ankitjain28may/getit/master/landscape.svg?style=flat-square)](https://landscape.io/github/ankitjain28may/getit/master)

A cross platform CLI downloader tool written in python 3

Installation
============

* Using `pip`

    ```shell
    $ pip install getit
    ```

* From source

    ```shell
    $ git clone https://github.com/ankitjain28may/getit
    $ cd getit
    $ python setup.py install
    ```
* For Setting Extra Utilities like Open File and Folder after the Download Completes..

    1- Get the path of the getit using `where` for linux users and `which` for window users.

    2- Copy the directory path where getit is present.

    3- copy the file from `https://raw.githubusercontent.com/ankitjain28may/getit/master/config.cfg` to `Directory_Path\config.cfg`.

    4- Set `True` or `False` according to your choice.


    ```shell
    $ where getit
    $ Directory_path/getit
    $ getit -d https://raw.githubusercontent.com/ankitjain28may/getit/master/config.cfg -p Directory_Path -f config.cfg
    ```


Usage
======

` getit -d <download url> -p <path> -f <filename with extension> `

` getit -h <help> `


Note : File is downloaded in the Downloads/getit/ folder by default

License
========

Copyright (c) 2016 Ankit Jain - Released under MIT License

P.S For more python scripts Go To -> [pythonResources](https://github.com/ankitjain28may/pythonResources)

