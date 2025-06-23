# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import socket as socketlib
import ssl
from typing import Optional, Union

from ._connection import DEFAULT_TIMEOUT, AbstractGvmConnection

DEFAULT_GVM_PORT = 9390
DEFAULT_HOSTNAME = "127.0.0.1"
DEFAULT_KNOWN_HOSTS_FILE = ".ssh/known_hosts"

logger = logging.getLogger("gvm.connections.tls")


class TLSConnection(AbstractGvmConnection):
    """
    TLS class to connect, read and write from a remote GVM daemon via TLS
    secured socket.
    """

    def __init__(
        self,
        *,
        certfile: Optional[str] = None,
        cafile: Optional[str] = None,
        keyfile: Optional[str] = None,
        hostname: Optional[str] = DEFAULT_HOSTNAME,
        port: Optional[int] = DEFAULT_GVM_PORT,
        password: Optional[str] = None,
        timeout: Optional[Union[int, float]] = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Create a new TLSConnection instance.

        Args:
            timeout: Timeout in seconds for the connection.
            hostname: DNS name or IP address of the remote TLS server.
            port: Port for the TLS connection. Default is 9390.
            certfile: Path to PEM encoded certificate file. See
                `python certificates <https://docs.python.org/3/library/ssl.html#certificates>`_ for details.
            cafile: Path to PEM encoded CA file. See `python certificates <https://docs.python.org/3/library/ssl.html#certificates>`_
                for details.
            keyfile: Path to PEM encoded private key. See `python certificates <https://docs.python.org/3/library/ssl.html#certificates>`_
                for details.
            password: Password for the private key. If the password argument is not
                specified and a password is required it will be interactively prompt
                the user for a password.
        """
        super().__init__(timeout=timeout)

        self.hostname = hostname if hostname is not None else DEFAULT_HOSTNAME
        self.port = port if port is not None else DEFAULT_GVM_PORT
        self.certfile = certfile
        self.cafile = cafile
        self.keyfile = keyfile
        self.password = password

    def _new_socket(self) -> ssl.SSLSocket:
        transport_socket = socketlib.socket(
            socketlib.AF_INET, socketlib.SOCK_STREAM
        )

        if self.certfile and self.cafile and self.keyfile:
            context = ssl.create_default_context(
                ssl.Purpose.SERVER_AUTH, cafile=self.cafile
            )
            context.check_hostname = False
            context.load_cert_chain(
                certfile=self.certfile,
                keyfile=self.keyfile,
                password=self.password,
            )
            context.minimum_version = ssl.TLSVersion.TLSv1_2
        else:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

        sock = context.wrap_socket(transport_socket, server_side=False)

        sock.settimeout(self._timeout)

        return sock

    def connect(self) -> None:
        self._socket = self._new_socket()
        self._socket.connect((self.hostname, int(self.port)))

    def disconnect(self):
        """Close the SSL layer then disconnect from the remote server"""
        try:
            if self._socket is not None:
                self._socket = self._socket.unwrap()
        except OSError as e:
            logger.debug("Connection closing error: %s", e)
        return super().disconnect()
