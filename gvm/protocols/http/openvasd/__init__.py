# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Package for sending requests to openvasd and handling HTTP API responses.

Modules:
- :class:`OpenvasdHttpApiV1` – Main class for communicating with OpenVASD API v1.

Usage:
    from gvm.protocols.http.openvasd import OpenvasdHttpApiV1
"""

from .openvasd1 import OpenvasdHttpAPIv1

__all__ = ["OpenvasdHttpAPIv1"]
