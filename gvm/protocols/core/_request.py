# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Protocol, runtime_checkable


@runtime_checkable
class Request(Protocol):
    """
    A GMP Request Python Protocol

    A Request implementation may be provided by several classes
    """

    def __bytes__(self) -> bytes: ...
