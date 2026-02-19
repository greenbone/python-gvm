# How to Use python-gvm

**python-gvm** lets you control a Greenbone Vulnerability Management (GVM) server from Python using the GMP or OSP protocols.

---

## Installation

```bash
python3 -m pip install python-gvm
```

---

## Connection Types

Pick the connection type that matches your setup:

| Type | When to use |
|------|-------------|
| `UnixSocketConnection` | gvmd runs on the same machine (fastest) |
| `TLSConnection` | Remote server over a secure TCP connection |
| `SSHConnection` | Remote server through an SSH tunnel |

---

## GMP – Greenbone Management Protocol

### 1. Simple request (no authentication)

```python
from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import GMP

connection = UnixSocketConnection(path='/run/gvmd/gvmd.sock')

with GMP(connection=connection) as gmp:
    print(gmp.get_version())
```

Expected output:
```xml
<get_version_response status="200" status_text="OK"><version>22.4</version></get_version_response>
```

---

### 2. Authenticated request

Most GMP commands require authentication. Use `EtreeCheckCommandTransform` to get
Python-parseable XML objects and automatic error raising on bad responses.

```python
from gvm.connections import UnixSocketConnection
from gvm.errors import GvmError
from gvm.protocols.gmp import GMP
from gvm.transforms import EtreeCheckCommandTransform

connection = UnixSocketConnection(path='/run/gvmd/gvmd.sock')
transform = EtreeCheckCommandTransform()

try:
    with GMP(connection=connection, transform=transform) as gmp:
        gmp.authenticate('admin', 'password')

        # Get all tasks whose name contains "weekly"
        tasks = gmp.get_tasks(filter_string='name~weekly')

        for task in tasks.xpath('task'):
            print(task.find('name').text)

except GvmError as e:
    print(f'Error: {e}')
```

---

### 3. Remote connections

**TLS (TCP + certificate)**:

```python
from gvm.connections import TLSConnection

connection = TLSConnection(
    hostname='192.168.1.100',
    port=9390,
    certfile='/path/to/client.crt',
    keyfile='/path/to/client.key',
    cafile='/path/to/ca.crt',
)
```

**SSH tunnel**:

```python
from gvm.connections import SSHConnection

connection = SSHConnection(
    hostname='192.168.1.100',
    port=22,
    username='gmp',
    password='secret',
)
```

Both can be used as a drop-in replacement for `UnixSocketConnection` in any of the examples above.

---

## OSP – Open Scanner Protocol

```python
from gvm.connections import UnixSocketConnection
from gvm.protocols.latest import Osp

connection = UnixSocketConnection(path='/var/run/ospd-wrapper.sock')
osp = Osp(connection=connection)

with osp:
    print(osp.get_version())
    print(osp.get_scans())
```

---

## Response transforms

By default every method returns a raw UTF-8 string. Two transforms are available:

| Transform | Returns |
|-----------|---------|
| `EtreeTransform` | `lxml.etree` Element (parse freely, no error check) |
| `EtreeCheckCommandTransform` | `lxml.etree` Element + raises `GvmError` on failure |

```python
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print

transform = EtreeTransform()

with GMP(connection=connection, transform=transform) as gmp:
    version = gmp.get_version()
    pretty_print(version)   # nicely formatted XML output
```

---

## Error handling

All exceptions inherit from `gvm.errors.GvmError`:

| Exception | Cause |
|-----------|-------|
| `GvmClientError` | Bad request sent by the client |
| `GvmServerError` | Server returned an error status |
| `InvalidArgument` | A parameter has an invalid value |
| `RequiredArgument` | A required parameter is missing |

```python
from gvm.errors import GvmError, InvalidArgument

try:
    with GMP(connection=connection, transform=transform) as gmp:
        gmp.authenticate('admin', 'password')
        gmp.get_task(task_id='invalid-id')
except InvalidArgument as e:
    print(f'Bad argument: {e}')
except GvmError as e:
    print(f'GVM error: {e}')
```

---

## Debugging

Log all sent/received data to a file:

```python
import logging
from gvm.connections import UnixSocketConnection, DebugConnection
from gvm.protocols.gmp import GMP

logging.basicConfig(filename='gvm_debug.log', level=logging.DEBUG)

connection = DebugConnection(UnixSocketConnection(path='/run/gvmd/gvmd.sock'))

with GMP(connection=connection) as gmp:
    gmp.get_version()
```

The log file will contain each raw command and response:

```
DEBUG:gvm.connections:Sending 14 characters. Data <get_version/>
DEBUG:gvm.connections:Read 97 characters. Data <get_version_response status="200" ...>
```

---

## More information

- Full API reference: <https://greenbone.github.io/python-gvm/>
- Community forum: <https://forum.greenbone.net/>
- Issue tracker: <https://github.com/greenbone/python-gvm/issues>
