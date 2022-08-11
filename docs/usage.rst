.. _usage:

Usage
=====

.. contents::
    :local:
    :class: toc
    :backlinks: none

Introduction
------------

To communicate with a remote server via one of the
:ref:`GVM protocols <Protocols>` it is required to decide which transport
protocol should be used for the :ref:`connection <Connections>`. Currently two protocols
– namely
:py:class:`GMP <gvm.protocols.gmpv214.Gmp>` and
:py:class:`OSP <gvm.protocols.ospv1.Osp>` – and three connection types – namely
:py:class:`TLS <gvm.connections.TLSConnection>`,
:py:class:`SSH <gvm.connections.SSHConnection>` and
:py:class:`Unix domain socket <gvm.connections.UnixSocketConnection>` –
are available.

Using GMP
---------

The **Greenbone Management Protocol (GMP)** is the protocol implemented by the
`Greenbone Vulnerability Manager Daemon – gvmd <https://github.com/greenbone/gvmd>`_.
It is also used by the `Greenbone Security Assistant Daemon <https://github.com/greenbone/gsa>`_
to request all of its information from **gvmd**.

Making a Simple Request
^^^^^^^^^^^^^^^^^^^^^^^

To create a request, a :ref:`connection <Connections>` type has to be chosen.
The decision depends on the location and configuration of the remote **gvmd**
server. For local communication :py:class:`Unix domain socket <gvm.connections.UnixSocketConnection>`
fits best. The simplest command is to request the **GMP** version used by the
remote **gvmd**.

Step by Step
""""""""""""

The following shows the process of a simple request in more detail.

1. Import the necessary classes:

.. code-block:: python

    from gvm.connections import UnixSocketConnection
    from gvm.protocols.gmp import Gmp

2. Specify the path to the Unix domain socket in the file system:

.. note:: If **gvmd** is provided by a package of the distribution, it should
    be ``/run/gvmd/gvmd.sock``. If **gvmd** was built from source and did not set
    a prefix, the default path can be used by setting ``path = None``.

.. code-block:: python

    path = '/run/gvmd/gvmd.sock'

3. Create a connection and a gmp object:

.. code-block:: python

    connection = UnixSocketConnection(path=path)

4. Establish a connection to be able to make a request on **gvmd**. To automatically connect and disconnect, a Python
   `with statement <https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers>`_ should be used.

.. note:: By default all request methods of the :py:class:`gmp <gvm.protocols.gmpv214.Gmp>`
    object return the response as UTF-8 encoded string.

5. Obtain the protocol version of the **gvmd** by printing the response of the unprivileged command ``*get_version*``:

.. code-block:: python

    with Gmp(connection=connection) as gmp:
        print(gmp.get_version())

Full Example
""""""""""""

.. code-block:: python

    from gvm.connections import UnixSocketConnection
    from gvm.protocols.gmp import Gmp

    # path to unix socket
    path = '/run/gvmd/gvmd.sock'
    connection = UnixSocketConnection(path=path)

    # using the with statement to automatically connect and disconnect to gvmd
    with Gmp(connection=connection) as gmp:
        # get the response message returned as a utf-8 encoded string
        response = gmp.get_version()

        # print the response message
        print(response)

On success the response will look as follows:

.. code-block:: xml

    <get_version_response status="200" status_text="OK"><version>9.0</version></get_version_response>

Privileged Request
^^^^^^^^^^^^^^^^^^

Most requests to **gvmd** require permissions to access data. Therefore it is
required to authenticate against **gvmd**.

Step by Step
""""""""""""

1. Import the necessary classes:

.. code-block:: python

    from gvm.connections import UnixSocketConnection
    from gvm.protocols.gmp import Gmp

2. Create a connection:

.. code-block:: python

    path = '/run/gvmd/gvmd.sock'
    connection = UnixSocketConnection(path=path)

3. In this case, an `Etree Element`_ should be obtained from the response to be able to
   extract specific information.

   To do so, pass a :py:mod:`transform <gvm.transforms>` to the :py:class:`Gmp <gvm.protocols.gmpv214.Gmp>`
   constructor. Additionally, a :py:class:`GvmError <gvm.errors.GvmError>` should be raised if the status of the
   response was not *ok*. Therefore choose a :py:class:`EtreeCheckCommandTransform <gvm.transforms.EtreeCheckCommandTransform>`:

.. code-block:: python

    from gvm.transforms import EtreeCheckCommandTransform

    transform = EtreeCheckCommandTransform()

.. note:: By choosing a :py:class:`EtreeCheckCommandTransform <gvm.transforms.EtreeCheckCommandTransform>` it is ensured that calling a privileged command always fails, e.g. calling

   .. code-block:: python

    with Gmp(connection=connection, transform=transform) as gmp:
       gmp.get_task()

   without being authenticated will throw an error now.

5. Set a user name and a password for authentication:

.. code-block:: python

    username = 'foo'
    password = 'bar'

6. Create a connection, do the authentication, request all tasks
   with 'weekly' in their name and list their full names:

.. code-block:: python

    from gvm.errors import GvmError

    try:
        with Gmp(connection=connection, transform=transform) as gmp:
            gmp.authenticate(username, password)

            tasks = gmp.get_tasks(filter_string='name~weekly')

            for task in tasks.xpath('task'):
                print(task.find('name').text)

    except GvmError as e:
        print('An error occurred', e)

.. _Etree Element:
    https://docs.python.org/3/library/xml.etree.elementtree.html#element-objects

Full Example
""""""""""""

.. code-block:: python

    import sys

    from gvm.connections import UnixSocketConnection
    from gvm.errors import GvmError
    from gvm.protocols.gmp import Gmp
    from gvm.transforms import EtreeCheckCommandTransform

    path = '/run/gvmd/gvmd.sock'
    connection = UnixSocketConnection(path=path)
    transform = EtreeCheckCommandTransform()

    username = 'foo'
    password = 'bar'

    try:
        tasks = []

        with Gmp(connection=connection, transform=transform) as gmp:
            gmp.authenticate(username, password)

            tasks = gmp.get_tasks(filter_string='name~weekly')

            for task in tasks.xpath('task'):
                print(task.find('name').text)

    except GvmError as e:
        print('An error occurred', e, file=sys.stderr)

Using OSP
---------

The **Open Scanner Protocol (OSP)** is a communication protocol implemented by
a base class for scanner wrappers `Open Scanner Protocol Daemon – ospd <https://github.com/greenbone/ospd>`_.
**OSP** creates a unified interface for different security scanners and makes
their control flow and scan results consistently available under the
`Greenbone Vulnerability Manager Daemon – gvmd <https://github.com/greenbone/gvmd>`_.
In many ways, **OSP** is similar to **Greenbone Management Protocol (GMP)**:
XML-based, stateless and with a non-permanent connection.

Making a Simple Request
^^^^^^^^^^^^^^^^^^^^^^^

To create a request you have to choose a :ref:`connection <connections>` type.
The decision depends on the location and configuration of the remote
**ospd-wrapper** server. For local communication :py:class:`Unix domain socket <gvm.connections.UnixSocketConnection>`
fits best, but also a :py:class:`secure TLS connection <gvm.connections.TLSConnection>`
is possible.
The simplest command is to request the server version.

Step by Step
""""""""""""

1. Import the necessary classes:

.. code-block:: python

    from gvm.connections import UnixSocketConnection
    from gvm.protocols.latest import Osp

2. The path to the Unix domain socket in the file system is given during the start
   of the ospd-wrapper.

   Specify the path to the Unix domain socket in the file system:

.. code-block:: python

    path = '/tmp/ospd-wrapper.sock'

3. Create a connection and an osp object:

.. code-block:: python

    connection = UnixSocketConnection(path=path)
    osp = Osp(connection=connection)

4. Establish a connection to be able to make a request on **ospd-wrapper**.
   To automatically connect and disconnect, a Python `with statement <https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers>`_
   should be used.

.. note:: By default all request methods of the :py:class:`osp <gvm.protocols.ospv1.Osp>`
    object return the response as UTF-8 encoded string.

5. Obtain the **OSP** protocol version, the **ospd** base implementation class and
   the **ospd-wrapper** server version by printing the response of the command ``get_version``:

.. code-block:: python

    with osp:
        print(osp.get_version())

Full Example
""""""""""""

.. code-block:: python

    from gvm.connections import UnixSocketConnection
    from gvm.protocols.latest import Osp

    # path to unix socket
    path = '/var/run/ospd-wrapper.sock'
    connection = UnixSocketConnection(path=path)
    osp = Osp(connection=connection)

    # using the with statement to automatically connect and disconnect to ospd
    with osp:
        # get the response message returned as a utf-8 encoded string
        response = osp.get_version()

        # print the response message
        print(response)

On success the response will look as follows:

.. code-block:: xml

    <get_version_response status="200" status_text="OK"><protocol><name>OSP</name><version>1.2</version></protocol><daemon><name>OSPd</name><version>1.4b1</version></daemon><scanner><name>some-wrapper</name><version>Wrapper 6.0beta+2</version></scanner></get_version_response>

Debugging
---------

Sometimes networking setups can be complex and hard to follow. Connections may
be aborted randomly or an invalid command may have arrived at the server side.
Because of this, it may be necessary to debug the connection handling and especially
the protocol commands.

**python-gvm** uses the `logging`_ package internally. To enable a
simple debug output appended to a *debug.log* file the following code can be
used:

.. code-block:: python

    import logging

    logging.basicConfig(filename='debug.log', level=logging.DEBUG)


With this simple addition it is already possible to debug ssh connection problems.

But what if a response did not contain the expected data and it is important to know
in detail which command has been send to the server?

In this case it is necessary to wrap the actual connection in a
:py:class:`DebugConnection <gvm.connections.DebugConnection>` class.

Example using GMP:

.. code-block:: python

    from gvm.connections import UnixSocketConnection, DebugConnection
    from gvm.protocols.gmp import Gmp

    path = '/run/gvmd/gvmd.sock'
    socketconnection = UnixSocketConnection(path=path)
    connection = DebugConnection(socketconnection)

    with Gmp(connection=connection) as gmp:
        gmp.get_version()

With this change the file *debug.log* will contain something as follows::

    DEBUG:gvm.connections:Sending 14 characters. Data <get_version/>
    DEBUG:gvm.connections:Read 97 characters. Data <get_version_response status="200" status_text="OK"><version>9.0</version></get_version_response>

.. _logging:
    https://docs.python.org/3/library/logging.html
