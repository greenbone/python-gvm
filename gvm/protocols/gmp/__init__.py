# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Protocol implementations for the Greenbone Management Protocol (GMP).

In most circumstances you will want to use the :class:`GMP` class which
dynamically selects the supported GMP protocol of the remote manager daemon.

If you need to use a specific GMP version, you can use the :class:`GMPv224` or
:class:`GMPv225` classes.

* :class:`GMP` - Dynamically select supported GMP protocol of the remote manager daemon.
* :class:`GMPv224` - GMP version 22.4
* :class:`GMPv225` - GMP version 22.5
"""

from ._gmp import GMP
from ._gmp224 import GMPv224
from ._gmp225 import GMPv225
from ._gmp226 import GMPv226

Gmp = GMP  # for backwards compatibility

__all__ = (
    "GMP",
    "Gmp",
    "GMPv224",
    "GMPv225",
    "GMPv226",
)
