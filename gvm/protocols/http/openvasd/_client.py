# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
http client for initializing a connection to the openvasd HTTP API.

HTTPS with mTLS is used by default. Plain HTTP can be enabled explicitly
with `insecure_http=True`.
"""

import ssl
from os import PathLike

from httpx import Client

StrOrPathLike = str | PathLike[str]


def create_openvasd_http_client(
    host_name: str,
    *,
    api_key: str | None = None,
    server_ca_path: StrOrPathLike | None = None,
    client_cert_paths: StrOrPathLike
    | tuple[StrOrPathLike, StrOrPathLike]
    | None = None,
    insecure_http: bool = False,
    port: int = 3000,
) -> Client:
    """
    Create a `httpx.Client` configured for the OpenVASD HTTP API.

    mTLS is used by default. Set `insecure_http=True` to use plain HTTP.
    In this case, an API key can be used for authorization.

    Args:
        host_name: Hostname or IP of the OpenVASD server (e.g., "localhost").
        api_key: Optional API key used for authentication via HTTP headers.
        server_ca_path: Path to the server's CA certificate (for verifying the server).
        client_cert_paths: Path to the client certificate (str) or a tuple of
                            (cert_path, key_path) for mTLS authentication.
        insecure_http: If True, disables SSL verification and uses HTTP instead of HTTPS.
        port: The port to connect to (default: 3000).

    Behavior:
        - If `insecure_http=True`, HTTP is used instead of HTTPS.
            An API key can be used for authorization.
        - If `insecure_http=False` (default), HTTPS with mTLS is used.
          Both `server_ca_path` and `client_cert_paths` are required.

    Raises:
        ValueError: If `insecure_http=False` and either
            `server_ca_path` or `client_cert_paths` is missing.
    """
    headers = {}
    if api_key:
        headers["X-API-KEY"] = api_key

    if insecure_http:
        return Client(
            base_url=f"http://{host_name}:{port}",
            headers=headers,
            http2=True,
            timeout=10.0,
        )

    if not server_ca_path or not client_cert_paths:
        raise ValueError(
            "Both server_ca_path and client_cert_paths must be provided "
            "when insecure_http is False."
        )
    # Prepare mTLS SSL context
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

    return Client(
        base_url=f"https://{host_name}:{port}",
        headers=headers,
        verify=context,
        http2=True,
        timeout=10.0,
    )
