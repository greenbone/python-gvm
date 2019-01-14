.. _install:

Installation of python-gvm
==========================

Using pip
---------

You can install the latest stable release of python-gvm from the Python Package
Index using `pip`_::

    pip install python-gvm


Using pipenv
------------

If you are developing an application or library that uses **python-gvm**
internally, it is often better to choose `pipenv`_ for handling your
dependencies.::

    pipenv install python-gvm

If you are not using `pipenv`_ yet, head over to the pipenv website for
installation instructions.

Getting the Source
------------------

The source code of python-gvm can be found at
`Github <https://github.com/greenbone/python-gvm>`_.

To clone the public repository run::

    git clone git://github.com/greenbone/python-gvm

Once you have a copy of the source, you can embed it in your own application::

    pip install -e /path/to/python-gvm

.. _pip: https://pip.pypa.io/
.. _pipenv: http://pipenv.org/
