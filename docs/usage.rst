.. _usage:

Usage
=====

.. contents::
    :local:
    :class: toc
    :backlinks: none

Introduction
------------

To communicate with a remote server speaking one of the
:ref:`GVM Protocols <protocols>` it is required to decide which transport
protocol to use for the :ref:`connection <connections>`. Currently two protocols
- namely
:py:class:`GMP <gvm.protocols.gmpv7.Gmp>` and
:py:class:`OSP <gvm.protocols.ospv1.Osp>` - and three connection types - namely
:py:class:`TLS <gvm.connections.TLSConnection>`,
:py:class:`SSH <gvm.connections.SSHConnection>` and
:py:class:`Unix domain socket <gvm.connections.UnixSocketConnection>` -
are available.

GMP
---

The **Greenbone Management Protocol - GMP** is the protocol implemented by the
`Greenbone Vulnerability Manager Daemon - gvmd <https://github.com/greenbone/gvmd>`_.
Therefore it's also used by the `Greenbone Security Assistant Daemon <https://github.com/greenbone/gsa>`_
to request all of its information from **gvmd**.

Make a simple request
^^^^^^^^^^^^^^^^^^^^^

To create a request you have to choose a :ref:`connection <connections>` type.
The decision depends on the location and configuration of the remote **gvmd**
server. For local communication :py:class:`Unix domain socket <gvm.connections.UnixSocketConnection>`
fits best. The simplest command is to request the **GMP** version used by the
remote **gvmd**.

Step by Step
""""""""""""

Beginning by importing the necessary classes

.. code-block:: python

    from gvm.connections import UnixSocketConnection
    from gvm.protocols.latest import Gmp

Afterwards we have to specify the path to the Unix domain socket in the
filesystem. If **gvmd** is provided by a package of your distribution it should
be ``/var/run/gvmd.sock``. If you did build **gvmd** from source and didn't set
a prefix you can use the default path by setting ``path = None``.

.. code-block:: python

    path = '/var/run/gvmd.sock'

Now we can create a connection and a gmp object:

.. code-block:: python

    connection = UnixSocketConnection(path=path)
    gmp = Gmp(connection=connection)

To be able to make a request on **gvmd** a connection must be established. To
automatically connect and disconnect a Python
`with statement <https://docs.python.org/3.5/reference/datamodel.html#with-statement-context-managers>`_
should be used.

By default all request methods of the :py:class:`gmp <gvm.protocols.gmpv7.Gmp>`
object return the response as utf-8 encoded string.

To get the protocol version of the **gvmd** we can print the response of the
unprivileged *get_version* command

.. code-block:: python

    with gmp:
        print(gmp.get_version())

Full example
""""""""""""

.. code-block:: python

    from gvm.connections import UnixSocketConnection
    from gvm.protocols.latest import Gmp

    # path to unix socket
    path = '/var/run/gvmd.sock'
    connection = UnixSocketConnection(path=path)
    gmp = Gmp(connection=connection)

    # using the with statement to automatically connect and disconnect to gvmd
    with gmp:
        # get the response message returned as a utf-8 encoded string
        response = gmp.get_version()

        # print the response message
        print(response)

On success the response will look like:

.. code-block:: xml

    <get_version_response status="200" status_text="OK"><version>7.0</version></get_version_response>

Privileged request
^^^^^^^^^^^^^^^^^^

Most requests to **gvmd** require permissions to access data. Therefore it is
required to authenticate against **gvmd**.

Step by Step
""""""""""""

Beginning by importing the necessary classes

.. code-block:: python

    from gvm.connections import UnixSocketConnection
    from gvm.protocols.latest import Gmp

and creating the connection

.. code-block:: python

    path = '/var/run/gvmd.sock'
    connection = UnixSocketConnection(path=path)

This time we want to get an `Etree Element`_ from the response to be able to
extract specific information. Therefore we need to pass a
:py:mod:`transform <gvm.transforms>` to the :py:class:`Gmp <gvm.protocols.gmpv7.Gmp>`
constructor. Additionally we want to raise a :py:class:`GvmError <gvm.errors.GvmError>`
if the status of the response was not *ok*. Therefore we choose a
:py:class:`EtreeCheckCommandTransform <gvm.transforms.EtreeCheckCommandTransform>`.

.. code-block:: python

    from gvm.transforms import EtreeCheckCommandTransform

    transform = EtreeCheckCommandTransform()
    gmp = Gmp(connection=connection, transform=transform)

By choosing a :py:class:`EtreeCheckCommandTransform <gvm.transforms.EtreeCheckCommandTransform>`
we ensure that calling a privileged command always fails. E.g. calling

.. code-block:: python

    gmp.get_task()

without being authenticated will throw an error now. For authentication we need
to set a username and password.


.. code-block:: python

    username = 'foo'
    password = 'bar'

Afterwards we can create a connection, do the authentication, request all tasks
with 'weekly' in their name and list their full names.

.. code-block:: python

    from gvm.errors import GvmError

    try:
        with gmp:
            gmp.authenticate(username, password)

            tasks = gmp.get_tasks(filter='name~weekly')

            for task in tasks.xpath('task'):
                print(task.find('name').text)

    except GvmError as e:
        print('An error occurred', str(e))

.. _Etree Element:
    https://docs.python.org/3.4/library/xml.etree.elementtree.html#element-objects

Full example
""""""""""""

.. code-block:: python

    from gvm.connections import UnixSocketConnection
    from gvm.errors import GvmError
    from gvm.protocols.latest import Gmp
    from gvm.transforms import EtreeCheckCommandTransform

    path = '/var/run/gvmd.sock'
    connection = UnixSocketConnection(path=path)
    transform = EtreeCheckCommandTransform()
    gmp = Gmp(connection=connection, transform=transform)

    username = 'foo'
    password = 'bar'

    try:
        tasks = []

        with gmp:
            gmp.authenticate(username, password)

            tasks = gmp.get_tasks(filter='name~weekly')

            for task in tasks.xpath('task'):
                print(task.find('name').text)

    except GvmError as e:
        print('An error occurred', str(e))

OSP
---

The **Open Scanner Protocol - OSP** is a communication protocol implemented by
a base class for scanner wrappers `Open Scanner Protocol Daemon- ospd <https://github.com/greenbone/ospd>`_.
**OSP** creates a unified interface for different security scanners and makes
their control flow and scan results consistently available under the
`Greenbone Vulnerability Manager Daemon - gvmd <https://github.com/greenbone/gvmd>`_.
**OSP** is similar in many ways to **Greenbone Management Protocol -GMP** :
XML-based, stateless and non-permanent connection.

Make a simple request
^^^^^^^^^^^^^^^^^^^^^

To create a request you have to choose a :ref:`connection <connections>` type.
The decision depends on the location and configuration of the remote
**ospd-wrapper** server. For local communication :py:class:`Unix domain socket <gvm.connections.UnixSocketConnection>`
fits best, but also a :py:class:`secure TLS connection <gvm.connections.TLSConnection>`
is possible.
The simplest command is to request the server version.

Step by Step
""""""""""""

Beginning by importing the necessary classes

.. code-block:: python

    from gvm.connections import UnixSocketConnection
    from gvm.protocols.latest import Osp

Afterwards we have to specify the path to the Unix domain socket in the
filesystem. This is the path given during the start of the ospd-wrapper.

.. code-block:: python

    path = '/tmp/ospd-wrapper.sock'

Now we can create a connection and a osp object:

.. code-block:: python

    connection = UnixSocketConnection(path=path)
    osp = Osp(connection=connection)

To be able to make a request on **ospd-wrapper** a connection must be
established. To automatically connect and disconnect, a Python
`with statement <https://docs.python.org/3.5/reference/datamodel.html#with-statement-context-managers>`_
should be used.

By default all request methods of the :py:class:`osp <osp.protocols.ospv1.Osp>`
object return the response as utf-8 encoded string.

It is possible to get the **OSP** protocol version, the
**ospd** base implementation class and the **ospd-wrapper** server version,
printing the response of the *get_version* command.

.. code-block:: python

    with osp:
        print(osp.get_version())

Full example
""""""""""""

.. code-block:: python

    from osp.connections import UnixSocketConnection
    from osp.protocols.latest import Osp

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

On success the response will look like:

.. code-block:: xml

    <get_version_response status="200" status_text="OK"><protocol><name>OSP</name><version>1.2</version></protocol><daemon><name>OSPd</name><version>1.4b1</version></daemon><scanner><name>some-wrapper</name><version>Wrapper 6.0beta+2</version></scanner></get_version_response>
