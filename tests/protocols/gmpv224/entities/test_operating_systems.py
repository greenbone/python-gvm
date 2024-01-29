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
from ...gmpv224 import Gmpv224TestCase


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
