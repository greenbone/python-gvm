# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from enum import Enum as PythonEnum
from typing import Any, Optional, Type, TypeVar

from gvm.errors import InvalidArgument

Self = TypeVar("Self", bound="Enum")


class Enum(PythonEnum):
    """
    Base class for Enums in python-gvm
    """

    @classmethod
    def _missing_(cls: Type[Self], value: Any) -> Optional[Self]:
        if isinstance(value, PythonEnum):
            return cls.from_string(value.name)
        return cls.from_string(str(value) if value else None)

    @classmethod
    def from_string(
        cls: Type[Self],
        value: Optional[str],
    ) -> Optional[Self]:
        """
        Convert a string value into an Enum instance

        If value is None or empty None is returned
        """
        if not value:
            return None

        try:
            return cls[value.replace(" ", "_").upper()]
        except KeyError:
            raise InvalidArgument(
                f"Invalid argument {value}. "
                f"Allowed values are {','.join(e.name for e in cls)}."
            ) from None

    def __str__(self) -> str:
        return self.value
