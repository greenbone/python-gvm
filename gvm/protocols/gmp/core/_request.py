# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Protocol, runtime_checkable


@runtime_checkable
class Request(Protocol):
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
