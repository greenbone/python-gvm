# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
http client for initializing a connection to the openvasd HTTP API using optional mTLS authentication.
"""

import ssl
from os import PathLike
from typing import Optional, Tuple, Union

from httpx import Client

StrOrPathLike = Union[str, PathLike[str]]


def create_openvasd_http_client(
    host_name: str,
    *,
    api_key: Optional[str] = None,
    server_ca_path: Optional[StrOrPathLike] = None,
    client_cert_paths: Optional[
        Union[StrOrPathLike, Tuple[StrOrPathLike, StrOrPathLike]]
    ] = None,
    port: int = 3000,
) -> Client:
    """
    Create a `httpx.Client` configured for mTLS-secured or API KEY access
    to an openvasd HTTP API instance.

    Args:
        host_name: Hostname or IP of the OpenVASD server (e.g., "localhost").
        api_key: Optional API key used for authentication via HTTP headers.
        server_ca_path: Path to the server's CA certificate (for verifying the server).
        client_cert_paths: Path to the client certificate (str) or a tuple of
                            (cert_path, key_path) for mTLS authentication.
        port: The port to connect to (default: 3000).

    Behavior:
        - If both `server_ca_path` and `client_cert_paths` are set, an mTLS connection
            is established using an SSLContext.
        - If not, `verify` is set to False (insecure), and HTTP is used instead of HTTPS.
            HTTP connection needs api_key for authorization.
    """
    headers = {}

    context: Optional[ssl.SSLContext] = None

    # Prepare mTLS SSL context if needed
    if client_cert_paths and server_ca_path:
        context = ssl.create_default_context(
            ssl.Purpose.SERVER_AUTH, cafile=server_ca_path
        )
        if isinstance(client_cert_paths, tuple):
            context.load_cert_chain(
                certfile=client_cert_paths[0], keyfile=client_cert_paths[1]
            )
        else:
            context.load_cert_chain(certfile=client_cert_paths)

        context.check_hostname = False
        context.verify_mode = ssl.CERT_REQUIRED

    # Set verify based on context presence
    verify: Union[bool, ssl.SSLContext] = context if context else False

    if api_key:
        headers["X-API-KEY"] = api_key

    protocol = "https" if context else "http"
    base_url = f"{protocol}://{host_name}:{port}"

    return Client(
        base_url=base_url,
        headers=headers,
        verify=verify,
        http2=True,
        timeout=10.0,
    )
