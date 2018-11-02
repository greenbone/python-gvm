.. _api:

Developer Interface
===================

This part of the documentation covers all public interfaces of gvm-tools.


Main
----

.. automodule:: gvm

.. autodata:: VERSION

.. autofunction:: get_version

Connections
-----------

.. automodule:: gvm.connections

.. autoclass:: GvmConnection
   :members:

.. autoclass:: SSHConnection
   :members:
   :inherited-members:

.. autoclass:: TLSConnection
   :members:
   :inherited-members:

.. autoclass:: UnixSocketConnection
   :members:
   :inherited-members:

Transforms
----------

.. automodule:: gvm.transforms
    :members:

Protocols
---------

.. automodule:: gvm.protocols

Latest
^^^^^^

.. automodule:: gvm.protocols.latest

GMP v7
^^^^^^

.. automodule:: gvm.protocols.gmpv7

.. autoclass:: Gmp
    :members:
    :inherited-members:

OSP v1
^^^^^^

.. automodule:: gvm.protocols.ospv1

.. autoclass:: Osp
    :members:
    :inherited-members:

Errors
------

.. automodule:: gvm.errors
    :members:

Utils
-----

.. automodule:: gvm.utils
    :members:

XML
---

.. automodule:: gvm.xml
    :members:
