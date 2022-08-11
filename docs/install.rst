.. _install:

Installation of python-gvm
==========================

For installing the latest stable release of **python-gvm**, `pip`_, `poetry`_
or `pipenv`_ can be used.

If an application or library that uses **python-gvm** internally is developed,
it is often better to choose `poetry`_ for handling the dependencies.

Using pip
---------

For installing **python-gvm** using `pip`_ run::

    python3 -m pip install python-gvm

Using poetry
------------

For installing **python-gvm** using `poetry`_ run::

    poetry add python-gvm

If the usage of `poetry`_ is not familiar, its documentation can be found at
https://python-poetry.org/docs/.

Using pipenv
------------

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

    python3 -m pip install -e /path/to/python-gvm

.. _pip: https://pip.pypa.io/en/stable/
.. _pipenv: https://pipenv.readthedocs.io/en/latest/
.. _poetry: https://python-poetry.org/
