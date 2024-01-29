# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.operating_systems import (
    GmpDeleteOperatingSystemTestMixin,
    GmpGetOperatingSystemsTestMixin,
    GmpGetOperatingSystemTestMixin,
    GmpModifyOperatingSystemTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225DeleteOperatingSystemTestCase(
    GmpDeleteOperatingSystemTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetOperatingSystemTestCase(
    GmpGetOperatingSystemTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetOperatingSystemsTestCase(
    GmpGetOperatingSystemsTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyOperatingSystemTestCase(
    GmpModifyOperatingSystemTestMixin, Gmpv225TestCase
):
    pass
