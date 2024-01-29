# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .operating_systems import (
    GmpDeleteOperatingSystemTestMixin,
    GmpGetOperatingSystemsTestMixin,
    GmpGetOperatingSystemTestMixin,
    GmpModifyOperatingSystemTestMixin,
)


class Gmpv208DeleteOperatingSystemTestCase(
    GmpDeleteOperatingSystemTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetOperatingSystemTestCase(
    GmpGetOperatingSystemTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetOperatingSystemsTestCase(
    GmpGetOperatingSystemsTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyOperatingSystemTestCase(
    GmpModifyOperatingSystemTestMixin, Gmpv208TestCase
):
    pass
