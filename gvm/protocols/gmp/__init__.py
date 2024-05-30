# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from ._gmp import GMP
from ._gmp224 import GMPv224
from ._gmp225 import GMPv225

Gmp = GMP  # for backwards compatibility

__all__ = (
    "GMP",
    "Gmp",
    "GMPv224",
    "GMPv225",
)
