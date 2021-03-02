pl-sevstack
================================

.. image:: https://img.shields.io/docker/v/fnndsc/pl-sevstack?sort=semver
    :target: https://hub.docker.com/r/fnndsc/pl-sevstack

.. image:: https://img.shields.io/github/license/fnndsc/pl-sevstack
    :target: https://github.com/FNNDSC/pl-sevstack/blob/master/LICENSE

.. image:: https://github.com/FNNDSC/pl-sevstack/workflows/ci/badge.svg
    :target: https://github.com/FNNDSC/pl-sevstack/actions


.. contents:: Table of Contents


Abstract
--------

This app will be a plugin that will take a large number of severity reports from pl-covidnet and their corresponding image files and create a ranked list of the the most severe Covid patients, so that doctors can tend to the most vulnerable patients first.


Description
-----------

``sevstack`` is a ChRIS-based application that...


Usage
-----

.. code::

    python sevstack.py
        [-h|--help]
        [--json] [--man] [--meta]
        [--savejson <DIR>]
        [-v|--verbosity <level>]
        [--version]
        <inputDir> <outputDir>


Arguments
~~~~~~~~~

.. code::

    [-h] [--help]
    If specified, show help message and exit.
    
    [--json]
    If specified, show json representation of app and exit.
    
    [--man]
    If specified, print (this) man page and exit.

    [--meta]
    If specified, print plugin meta data and exit.
    
    [--savejson <DIR>] 
    If specified, save json representation file to DIR and exit. 
    
    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.
    
    [--version]
    If specified, print version number and exit. 


Getting inline help is:

.. code:: bash

    docker run --rm fnndsc/pl-sevstack sevstack --man

Run
~~~

You need you need to specify input and output directories using the `-v` flag to `docker run`.


.. code:: bash

    docker run --rm -u $(id -u)                             \
        -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
        local/pl-sevstack sevstack                        \
        /in /out

.. code:: bash

   docker run --rm -u $(id -u)				\ 
	-v $(pwd)/sevstack:/usr/local/lib/python3.9/site-packages/sevstack:ro -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing	\ 
	local/pl-sevstack sevstack			\ 
	in out

docker run --rm -u $(id -u) -ti                         \
        -v $(pwd)/sevstack:/usr/local/lib/python3.9/site-packages/sevstack:ro -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing    \
        local/pl-sevstack sevstack                      \
        /in /out


Development
-----------

Build the Docker container:

.. code:: bash

    docker build -t local/pl-sevstack .

Run unit tests:

.. code:: bash

    docker run --rm local/pl-sevstack nosetests

Examples
--------

Put some examples here!


.. image:: https://raw.githubusercontent.com/FNNDSC/cookiecutter-chrisapp/master/doc/assets/badge/light.png
    :target: https://chrisstore.co
