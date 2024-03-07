# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from ._gmp import GMP

Gmp = GMP  # for backwards compatibility

__all__ = (
    "GMP",
    "Gmp",
)
