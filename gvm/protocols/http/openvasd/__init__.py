# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
High-level API interface for interacting with openvasd HTTP services via
logical modules (health, metadata, scans, etc.).

Usage:

.. code-block:: python

    from gvm.protocols.http.openvasd import OpenvasdHttpAPIv1
"""

from ._openvasd1 import OpenvasdHttpAPIv1

__all__ = ["OpenvasdHttpAPIv1"]
