# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.operating_systems import (
    GmpDeleteOperatingSystemTestMixin,
    GmpGetOperatingSystemsTestMixin,
    GmpGetOperatingSystemTestMixin,
    GmpModifyOperatingSystemTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214DeleteOperatingSystemTestCase(
    GmpDeleteOperatingSystemTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetOperatingSystemTestCase(
    GmpGetOperatingSystemTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetOperatingSystemsTestCase(
    GmpGetOperatingSystemsTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyOperatingSystemTestCase(
    GmpModifyOperatingSystemTestMixin, Gmpv214TestCase
):
    pass
