.. _usage:

Usage
=====

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

Privileged request
^^^^^^^^^^^^^^^^^^

Most requests to gvmd require permissions to access data. Therefore it is
required to authenticate against gvmd.

OSP
---

Make a simple request
^^^^^^^^^^^^^^^^^^^^^
