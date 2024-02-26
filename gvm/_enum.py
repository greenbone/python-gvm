# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from enum import Enum as PythonEnum
from typing import Optional

from typing_extensions import Self

from gvm.errors import InvalidArgument


class Enum(PythonEnum):
    """
    Base class for Enums in python-gvm
    """

    @classmethod
    def from_string(
        cls,
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
                f"Invalid argument {value} for {cls.__name__}.from_string. "
                f"Allowed values are {','.join(e.name for e in cls)}."
            ) from None
