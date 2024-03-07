# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from ._connection import DEFAULT_TIMEOUT, GvmConnection
from ._debug import DebugConnection
from ._ssh import (
    DEFAULT_HOSTNAME,
    DEFAULT_KNOWN_HOSTS_FILE,
    DEFAULT_SSH_PASSWORD,
    DEFAULT_SSH_PORT,
    DEFAULT_SSH_USERNAME,
    SSHConnection,
)
from ._tls import DEFAULT_GVM_PORT, TLSConnection
from ._unix import DEFAULT_UNIX_SOCKET_PATH, UnixSocketConnection

__all__ = (
    "DEFAULT_TIMEOUT",
    "DEFAULT_UNIX_SOCKET_PATH",
    "DEFAULT_GVM_PORT",
    "DEFAULT_HOSTNAME",
    "DEFAULT_KNOWN_HOSTS_FILE",
    "DEFAULT_SSH_PASSWORD",
    "DEFAULT_SSH_USERNAME",
    "DEFAULT_SSH_PORT",
    "DebugConnection",
    "GvmConnection",
    "SSHConnection",
    "TLSConnection",
    "UnixSocketConnection",
)
