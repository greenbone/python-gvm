.. _install:

Installation of python-gvm
==========================

.. contents::
    :local:
    :class: toc
    :backlinks: none

.. note:: All commands listed here use the general tool names. If some of these
  tools are provided by the distribution, the Python 3 version of the tool may 
  have to be used, e.g. :program:`pip3`.
  
Installing the Latest Stable Release of python-gvm
--------------------------------------------------

For installing the latest stable release of **python-gvm**, `pip`_ or `pipenv`_
can be used.

If an appliacation or library that uses **python-gvm** internally is developed,
it is often better to choose `pipenv`_ for handling the dependencies.

Using pip
^^^^^^^^^

For installing **python-gvm** using `pip`_ run::

    pip install python-gvm


Using pipenv
^^^^^^^^^^^^

For installing **python-gvm** using `pipenv`_ run::

    pipenv install python-gvm

If `pipenv`_ is not used yet, head over to the pipenv website for
installation instructions.

Getting the Source
------------------

The source code of **python-gvm** can be found at
`GitHub <https://github.com/greenbone/python-gvm>`_.

To clone the public repository run::

    git clone git://github.com/greenbone/python-gvm

Once there is a copy of the source, it can be embedded it the own application as follows::

    pip install -e /path/to/python-gvm

.. _pip: https://pip.pypa.io/en/stable/
.. _pipenv: http://pipenv.org/
