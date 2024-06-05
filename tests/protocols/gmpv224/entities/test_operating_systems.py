# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .operating_systems import (
    GmpDeleteOperatingSystemTestMixin,
    GmpGetOperatingSystemsTestMixin,
    GmpGetOperatingSystemTestMixin,
    GmpModifyOperatingSystemTestMixin,
)


class Gmpv224DeleteOperatingSystemTestCase(
    GmpDeleteOperatingSystemTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetOperatingSystemTestCase(
    GmpGetOperatingSystemTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetOperatingSystemsTestCase(
    GmpGetOperatingSystemsTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyOperatingSystemTestCase(
    GmpModifyOperatingSystemTestMixin, Gmpv224TestCase
):
    pass
